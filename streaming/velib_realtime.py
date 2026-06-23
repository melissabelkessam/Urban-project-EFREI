"""
Flux TEMPS RÉEL — Vélib' Métropole (GBFS public, sans clé) — C2.2
================================================================
Démonstrateur de streaming sur une VRAIE source de données ouverte temps réel :
le flux GBFS de Vélib' Métropole (~1400 stations, mis à jour chaque minute).

Contrairement à producer_consumer_demo.py (flux SIMULÉ pour illustrer les
paradigmes), ce script ingère un flux EXTERNE RÉEL :
  - Le producteur interroge l'API GBFS toutes les POLL_INTERVAL secondes
    et pousse chaque snapshot de station dans une file (queue.Queue).
  - Le consommateur TEMPS RÉEL traite chaque station dès son arrivée.
  - L'agrégateur MICRO-BATCH calcule, par fenêtre, le nombre de vélos et de
    bornes disponibles dans tout Paris.

Veille technologique (C2.2) : le standard industriel serait Kafka + un
connecteur source. À l'échelle pédagogique, une file en mémoire + threads
suffit à démontrer l'ingestion temps réel ET le micro-batch sur une source
réelle, sans infrastructure à déployer.

Robustesse : si l'API est injoignable (réseau coupé, blocage), le script
bascule automatiquement en mode dégradé simulé afin que la démonstration
ne s'interrompe jamais (utile en soutenance).

Lancer avec : python streaming/velib_realtime.py
Arrêter avec : Ctrl+C
"""
import threading
import queue
import time
import random
from datetime import datetime, timezone
from collections import defaultdict

import requests

# ─── Configuration ──────────────────────────────────────────────────────────
GBFS_URLS = [
    "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json",
    "https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_status.json",
]
POLL_INTERVAL = 30      # secondes entre deux interrogations de l'API (MAJ source = 1/min)
WINDOW_SECONDS = 10     # fenêtre tumbling pour le micro-batch
HTTP_TIMEOUT = 15

EVENT_QUEUE = queue.Queue()
microbatch_buffer = []
running = True
_mode = {"simule": False}   # passe à True si l'API est injoignable


# ─── Producteur : interroge le flux GBFS réel ───────────────────────────────
def fetch_stations():
    """Récupère la liste des stations depuis l'API GBFS (essaie chaque URL)."""
    for url in GBFS_URLS:
        try:
            r = requests.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": "UrbanDataExplorer/1.0"})
            r.raise_for_status()
            return r.json().get("data", {}).get("stations", [])
        except Exception as exc:
            print(f"[WARN] échec sur {url.split('/')[2]} : {exc}")
    return None


def _stations_simulees():
    """Génère des stations factices si l'API est injoignable (mode dégradé)."""
    return [
        {
            "station_id": f"sim-{i:04d}",
            "num_bikes_available": random.randint(0, 30),
            "num_docks_available": random.randint(0, 30),
            "is_renting": 1,
        }
        for i in range(1, 51)
    ]


def normaliser(s):
    """Normalise une station GBFS en événement métier propre."""
    return {
        "station_id": str(s.get("station_id", "")),
        "velos_dispo": s.get("num_bikes_available", 0),
        "bornes_dispo": s.get("num_docks_available", 0),
        "en_service": bool(s.get("is_renting", 0)),
        "event_time": datetime.now(timezone.utc).isoformat(),
    }


def producer():
    """Interroge l'API toutes les POLL_INTERVAL s et pousse chaque station."""
    while running:
        stations = fetch_stations()
        if stations is None:
            _mode["simule"] = True
            stations = _stations_simulees()
            print(f"[MODE DÉGRADÉ] API injoignable → {len(stations)} stations simulées")
        else:
            _mode["simule"] = False
            print(f"[FETCH] {len(stations)} stations réelles reçues du flux Vélib")

        for s in stations:
            EVENT_QUEUE.put(normaliser(s))

        for _ in range(POLL_INTERVAL):
            if not running:
                break
            time.sleep(1)


# ─── Consommateur TEMPS RÉEL ────────────────────────────────────────────────
def realtime_consumer():
    """Traite chaque station dès son arrivée dans la file."""
    traites = 0
    while running:
        try:
            event = EVENT_QUEUE.get(timeout=1)
        except queue.Empty:
            continue
        traites += 1
        # On n'affiche qu'1 station sur 200 pour ne pas noyer la console
        if traites % 200 == 0:
            etat = "service" if event["en_service"] else "hors-service"
            print(f"[TEMPS RÉEL] station {event['station_id']:<8} "
                  f"{event['velos_dispo']:>2} vélos / {event['bornes_dispo']:>2} bornes ({etat})")
        microbatch_buffer.append(event)
        EVENT_QUEUE.task_done()


# ─── Agrégateur MICRO-BATCH ─────────────────────────────────────────────────
def microbatch_aggregator():
    """Agrège par fenêtre tumbling : total vélos / bornes disponibles dans Paris."""
    window_no = 0
    while running:
        time.sleep(WINDOW_SECONDS)
        window_no += 1
        batch = microbatch_buffer[:]
        microbatch_buffer.clear()
        if not batch:
            print(f"[MICRO-BATCH #{window_no}] fenêtre {WINDOW_SECONDS}s — 0 événement")
            continue

        total_velos = sum(e["velos_dispo"] for e in batch)
        total_bornes = sum(e["bornes_dispo"] for e in batch)
        en_service = sum(1 for e in batch if e["en_service"])
        source = "SIMULÉ" if _mode["simule"] else "RÉEL"

        print(f"\n[MICRO-BATCH #{window_no}] source={source} · fenêtre {WINDOW_SECONDS}s — "
              f"{len(batch)} stations traitées")
        print(f"   → {total_velos:,} vélos disponibles · {total_bornes:,} bornes libres · "
              f"{en_service}/{len(batch)} stations en service\n")


if __name__ == "__main__":
    print("=" * 70)
    print("FLUX TEMPS RÉEL VÉLIB' — Urban Data Explorer (C2.2)")
    print(f"Source : API GBFS publique · poll {POLL_INTERVAL}s · fenêtre {WINDOW_SECONDS}s")
    print("Ctrl+C pour arrêter")
    print("=" * 70 + "\n")

    threads = [
        threading.Thread(target=producer, daemon=True),
        threading.Thread(target=realtime_consumer, daemon=True),
        threading.Thread(target=microbatch_aggregator, daemon=True),
    ]
    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
        print("\nArrêt du flux temps réel Vélib.")
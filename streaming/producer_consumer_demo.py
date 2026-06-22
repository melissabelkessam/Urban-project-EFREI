"""
Démonstrateur streaming / micro-batch — C2.2
Simule un flux d'événements (transactions immobilières) traité en temps réel
ET par micro-batch (fenêtres tumbling), sans dépendance externe (pas de Kafka).

Veille technologique : Kafka/RabbitMQ sont les standards industriels pour ce
type de flux, mais à l'échelle de ce projet pédagogique, une file en mémoire
(queue.Queue) + threads producteur/consommateurs suffit à illustrer les deux
paradigmes (temps réel + micro-batch) sans infrastructure à déployer.

Lancer avec : python streaming/producer_consumer_demo.py
Arrêter avec Ctrl+C.
"""
import threading
import queue
import random
import time
from datetime import datetime, timezone
from collections import defaultdict

EVENT_QUEUE = queue.Queue()
ARRONDISSEMENTS = list(range(1, 21))
WINDOW_SECONDS = 5
running = True
microbatch_buffer = []


def producer():
    """Simule l'arrivée d'événements (transactions immobilières) en continu."""
    event_id = 0
    while running:
        event_id += 1
        event = {
            "event_id": event_id,
            "arrondissement": random.choice(ARRONDISSEMENTS),
            "prix_m2": round(random.uniform(7500, 14500), 0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        EVENT_QUEUE.put(event)
        time.sleep(random.uniform(0.2, 0.8))


def realtime_consumer():
    """Traitement TEMPS RÉEL : chaque événement est traité dès son arrivée."""
    while running:
        try:
            event = EVENT_QUEUE.get(timeout=1)
        except queue.Empty:
            continue
        print(f"[TEMPS RÉEL] Vente arr.{event['arrondissement']:<2} "
              f"à {event['prix_m2']:>8.0f} €/m² — reçu à {event['timestamp']}")
        microbatch_buffer.append(event)
        EVENT_QUEUE.task_done()


def microbatch_aggregator():
    """Traitement MICRO-BATCH : agrège les événements par fenêtres tumbling."""
    window_no = 0
    while running:
        time.sleep(WINDOW_SECONDS)
        window_no += 1
        batch = microbatch_buffer[:]
        microbatch_buffer.clear()
        if not batch:
            print(f"[MICRO-BATCH #{window_no}] fenêtre de {WINDOW_SECONDS}s — 0 événement")
            continue

        agg = defaultdict(lambda: {"count": 0, "sum": 0.0})
        for e in batch:
            a = agg[e["arrondissement"]]
            a["count"] += 1
            a["sum"] += e["prix_m2"]

        print(f"\n[MICRO-BATCH #{window_no}] fenêtre de {WINDOW_SECONDS}s — "
              f"{len(batch)} événements sur {len(agg)} arrondissements :")
        for arr, vals in sorted(agg.items()):
            avg = vals["sum"] / vals["count"]
            print(f"   arr.{arr:<2} → {vals['count']} ventes, prix moyen {avg:,.0f} €/m²")
        print()


if __name__ == "__main__":
    print("=" * 70)
    print("DÉMONSTRATEUR STREAMING — Urban Data Explorer (C2.2)")
    print(f"Fenêtre micro-batch : {WINDOW_SECONDS}s · Ctrl+C pour arrêter")
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
        print("\nArrêt du démonstrateur streaming.")
"""
Producteur DISTRIBUE - Qualite de l'air -> broker Redis - C2.2
Ce producteur tourne dans son propre processus. Il interroge l'API WAQI/Airparif
(qualite de l'air temps reel parisienne) et publie chaque mesure sur un canal
Redis heberge (Upstash). Le consommateur tourne dans un autre processus et recoit
ces messages via le broker sur le reseau : vrai systeme distribue.

Lancer (1er terminal) : python streaming/air_redis_producer.py
Arreter avec Ctrl+C.
"""
import json
import os
import random
import time
from datetime import datetime, timezone

import redis
import requests
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CHANNEL = os.getenv("REDIS_CHANNEL", "air-quality-events")
WAQI_TOKEN = os.getenv("WAQI_TOKEN", "demo")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))
HTTP_TIMEOUT = 15

STATIONS = ["paris", "paris-7eme", "paris-18eme", "paris-13eme", "neuilly-sur-seine"]


def fetch_station(station):
    url = f"https://api.waqi.info/feed/{station}/?token={WAQI_TOKEN}"
    r = requests.get(url, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "ok":
        return None
    d = data["data"]
    iaqi = d.get("iaqi", {})
    return {
        "station": station,
        "aqi": d.get("aqi"),
        "no2": iaqi.get("no2", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "pm25": iaqi.get("pm25", {}).get("v"),
        "o3": iaqi.get("o3", {}).get("v"),
        "event_time": datetime.now(timezone.utc).isoformat(),
    }


def _mesure_simulee(station):
    return {
        "station": station,
        "aqi": random.randint(20, 90),
        "no2": round(random.uniform(10, 60), 1),
        "pm10": round(random.uniform(10, 40), 1),
        "pm25": round(random.uniform(5, 30), 1),
        "o3": round(random.uniform(20, 80), 1),
        "event_time": datetime.now(timezone.utc).isoformat(),
    }


def main():
    client = redis.from_url(REDIS_URL, decode_responses=True)
    client.ping()
    print(f"[PRODUCTEUR] connecte au broker Redis . canal '{CHANNEL}'")

    while True:
        for station in STATIONS:
            mesure = None
            try:
                mesure = fetch_station(station)
            except Exception as exc:
                print(f"[WARN] station '{station}' : {exc}")
            if mesure is None:
                mesure = _mesure_simulee(station)
            client.publish(CHANNEL, json.dumps(mesure))

        print(f"[PRODUCTEUR] {len(STATIONS)} mesures publiees sur '{CHANNEL}' a "
              f"{datetime.now().strftime('%H:%M:%S')}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[PRODUCTEUR] arret.")
    except redis.exceptions.RedisError as exc:
        print(f"[ERREUR REDIS] {exc}\nVerifie REDIS_URL dans ton .env")
#!/usr/bin/env python3
"""
Wazuh Alerts Feeder
Auteurs: Fadyl ROUFAI
Description: Script qui envoie les alertes Wazuh vers l'indexer OpenSearch
"""

import json
import os
import time
import urllib.request
import ssl
import base64
from datetime import datetime

# Configuration
INDEXER_URL = "https://127.0.0.1:9200"
USERNAME = "admin"
PASSWORD = "admin"
ALERTS_FILE = "/var/ossec/logs/alerts/alerts.json"

# Contexte SSL (certificats auto-signés)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Authentification
credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {credentials}"
}


def send_alert(alert):
    """Envoie une alerte vers l'indexer OpenSearch."""
    index = f"wazuh-alerts-4.x-{datetime.now().strftime('%Y.%m.%d')}"
    url = f"{INDEXER_URL}/{index}/_doc"
    alert["@timestamp"] = alert.get("timestamp", datetime.now().isoformat())
    data = json.dumps(alert).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        urllib.request.urlopen(req, context=ctx)
    except Exception as e:
        print(f"Erreur envoi alerte: {e}")


def tail_file(filename):
    """Lit le fichier d'alertes en temps réel."""
    with open(filename, 'r') as f:
        f.seek(0, 2)  # Aller à la fin du fichier
        while True:
            line = f.readline()
            if line:
                try:
                    alert = json.loads(line)
                    send_alert(alert)
                    print(f"Alerte envoyée: {alert.get('rule', {}).get('description', '')}")
                except json.JSONDecodeError:
                    pass
            else:
                time.sleep(1)


if __name__ == "__main__":
    print("Wazuh Feeder démarré — envoi des alertes vers l'indexer...")
    while not os.path.exists(ALERTS_FILE):
        print(f"En attente du fichier {ALERTS_FILE}...")
        time.sleep(5)
    tail_file(ALERTS_FILE)

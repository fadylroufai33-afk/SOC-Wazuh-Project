# 🏗️ Architecture du SOC Wazuh

## Vue d'ensemble

Notre SOC est composé de 4 composants principaux qui communiquent entre eux :

```
┌─────────────────────────────────────────────────────────────────┐
│                        RÉSEAU 172.20.10.0/28                    │
│                                                                  │
│  ┌──────────────┐    ┌──────────────────────────────────────┐   │
│  │ Agent Linux  │    │         SERVEUR WAZUH                │   │
│  │ Fadyl Laptop │───▶│  ┌────────────┐  ┌───────────────┐  │   │
│  │172.20.10.12  │    │  │   Manager  │  │    Indexer    │  │   │
│  └──────────────┘    │  │ (Cerveau)  │─▶│  (Mémoire)    │  │   │
│                      │  └────────────┘  └───────────────┘  │   │
│  ┌──────────────┐    │         │                ▲           │   │
│  │Agent Windows │    │         ▼                │           │   │
│  │Florine-Brie  │───▶│  ┌────────────┐          │           │   │
│  │172.20.10.11  │    │  │ Dashboard  │──────────┘           │   │
│  └──────────────┘    │  │  (Ecran)   │                      │   │
│                      │  └────────────┘                      │   │
│                      │  172.20.10.14                        │   │
│                      └──────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Rôle de chaque composant

### 📡 Les Agents
Installés sur chaque machine surveillée. Ils collectent tous les événements (connexions, fichiers modifiés, commandes exécutées) et les envoient au Manager.

### 🧠 Wazuh Manager
Le cerveau du système. Il reçoit les données des agents, applique les règles de détection et génère les alertes.

### 💾 Wazuh Indexer (OpenSearch)
La mémoire du système. Il stocke toutes les alertes dans une base de données consultable. Port 9200.

### 🖥️ Wazuh Dashboard
L'écran de contrôle. Interface web accessible sur `https://IP_SERVEUR`. Permet de visualiser les alertes en temps réel.

---

## Flux de données

```
Machine surveillée
       │
       │ Logs & événements
       ▼
  Wazuh Agent
       │
       │ Transmission chiffrée (port 1514)
       ▼
  Wazuh Manager
       │
       │ Analyse + application des règles
       ▼
  Alerte générée
       │
       │ Via wazuh-feeder.py
       ▼
  Wazuh Indexer
       │
       │ Stockage indexé
       ▼
  Wazuh Dashboard
       │
       │ Visualisation
       ▼
  Analyste SOC 👁️
```

---

## Infrastructure technique

| Composant | Technologie | Version |
|---|---|---|
| OS Serveur | Ubuntu | 22.04 LTS |
| Wazuh Manager | Wazuh | 4.14.5 |
| Base de données | OpenSearch | 2.19.5 |
| Interface web | OpenSearch Dashboards | 2.19.5 |
| Script feeder | Python | 3.x |
| Certificats SSL | OpenSSL | 3.0 |

---

## Ports utilisés

| Port | Service | Description |
|---|---|---|
| 443 | HTTPS | Accès au Dashboard |
| 1514 | TCP/UDP | Communication agents → manager |
| 1515 | TCP | Enregistrement des agents |
| 9200 | HTTPS | API OpenSearch |
| 9300 | TCP | Communication interne OpenSearch |

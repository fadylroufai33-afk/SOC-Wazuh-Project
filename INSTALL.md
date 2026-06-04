# 📖 Guide d'installation — SOC Wazuh 4.14.5

## Prérequis

- Ubuntu 22.04 LTS (8GB RAM minimum, 4 CPU, 50GB disque)
- Accès internet
- Droits sudo

---

## Étape 1 — Préparer le système

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install curl wget python3 -y
echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## Étape 2 — Installer Wazuh Manager

```bash
curl -sO https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-manager/wazuh-manager_4.14.5-1_amd64.deb
sudo dpkg -i wazuh-manager_4.14.5-1_amd64.deb
sudo systemctl enable wazuh-manager
sudo systemctl start wazuh-manager
```

---

## Étape 3 — Installer Wazuh Indexer

```bash
curl -sO https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-indexer/wazuh-indexer_4.14.5-1_amd64.deb
sudo dpkg -i wazuh-indexer_4.14.5-1_amd64.deb
```

---

## Étape 4 — Générer les certificats SSL

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-certs-tool.sh

cat > ~/config.yml << 'EOF'
nodes:
  indexer:
    - name: node-1
      ip: 127.0.0.1
  server:
    - name: wazuh-1
      ip: 127.0.0.1
  dashboard:
    - name: dashboard
      ip: 127.0.0.1
EOF

sudo bash wazuh-certs-tool.sh -A
```

---

## Étape 5 — Déployer les certificats

```bash
# Indexer
sudo mkdir -p /etc/wazuh-indexer/certs
sudo cp ~/wazuh-certificates/node-1.pem /etc/wazuh-indexer/certs/indexer.pem
sudo cp ~/wazuh-certificates/node-1-key.pem /etc/wazuh-indexer/certs/indexer-key.pem
sudo cp ~/wazuh-certificates/root-ca.pem /etc/wazuh-indexer/certs/root-ca.pem
sudo cp ~/wazuh-certificates/admin.pem /etc/wazuh-indexer/certs/admin.pem
sudo cp ~/wazuh-certificates/admin-key.pem /etc/wazuh-indexer/certs/admin-key.pem
sudo chown -R wazuh-indexer:wazuh-indexer /etc/wazuh-indexer/certs/

# Dashboard
sudo mkdir -p /etc/wazuh-dashboard/certs
sudo cp ~/wazuh-certificates/dashboard.pem /etc/wazuh-dashboard/certs/
sudo cp ~/wazuh-certificates/dashboard-key.pem /etc/wazuh-dashboard/certs/
sudo cp ~/wazuh-certificates/root-ca.pem /etc/wazuh-dashboard/certs/
sudo chown -R wazuh-dashboard:wazuh-dashboard /etc/wazuh-dashboard/certs/
```

---

## Étape 6 — Démarrer l'indexer

```bash
sudo systemctl enable wazuh-indexer
sudo systemctl start wazuh-indexer
sleep 30

# Initialiser la sécurité OpenSearch
sudo JAVA_HOME=/usr/share/wazuh-indexer/jdk \
  /usr/share/wazuh-indexer/plugins/opensearch-security/tools/securityadmin.sh \
  -cd /etc/wazuh-indexer/opensearch-security/ \
  -icl -nhnv \
  -cacert /etc/wazuh-indexer/certs/root-ca.pem \
  -cert /etc/wazuh-indexer/certs/admin.pem \
  -key /etc/wazuh-indexer/certs/admin-key.pem \
  -h 127.0.0.1 -p 9200
```

---

## Étape 7 — Installer le Dashboard

```bash
curl -sO https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-dashboard/wazuh-dashboard_4.14.5-1_amd64.deb
sudo dpkg -i wazuh-dashboard_4.14.5-1_amd64.deb
sudo systemctl enable wazuh-dashboard
sudo systemctl start wazuh-dashboard
```

---

## Étape 8 — Activer l'envoi des alertes

```bash
sudo cp scripts/wazuh-feeder.py /usr/local/bin/wazuh-feeder.py
sudo chmod +x /usr/local/bin/wazuh-feeder.py

# Créer le service systemd
sudo tee /etc/systemd/system/wazuh-feeder.service > /dev/null << 'EOF'
[Unit]
Description=Wazuh Alerts Feeder
After=wazuh-manager.service wazuh-indexer.service

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/wazuh-feeder.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable wazuh-feeder
sudo systemctl start wazuh-feeder
```

---

## Étape 9 — Installer un agent Linux

```bash
curl -sO https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.5-1_amd64.deb
sudo WAZUH_MANAGER='VOTRE_IP_SERVEUR' dpkg -i wazuh-agent_4.14.5-1_amd64.deb
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

---

## Étape 10 — Installer un agent Windows

Sur PowerShell en Admin :

```powershell
$IP_WAZUH = "VOTRE_IP_SERVEUR"
Invoke-WebRequest -Uri "https://packages.wazuh.com/4.x/windows/wazuh-agent-4.14.5-1.msi" -OutFile "wazuh-agent.msi"
msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER="$IP_WAZUH"
Start-Service Wazuh
```

---

## Vérification finale

```bash
# Vérifier tous les services
sudo systemctl status wazuh-manager wazuh-indexer wazuh-dashboard wazuh-feeder

# Vérifier les agents connectés
sudo /var/ossec/bin/agent_control -l

# Vérifier les alertes
curl -k -u admin:admin "https://localhost:9200/_cat/indices?v" | grep wazuh-alerts
```

---

## Accès au Dashboard

```
URL      : https://VOTRE_IP_SERVEUR
Login    : admin
Password : admin
```

---

## Dépannage

| Problème | Solution |
|---|---|
| Dashboard ne démarre pas | Vérifier les certs dans `/etc/wazuh-dashboard/certs/` |
| Pas d'alertes dans Discover | Relancer `sudo systemctl restart wazuh-feeder` |
| Agent non connecté | Vérifier l'IP dans `/var/ossec/etc/ossec.conf` |
| Indexer ne répond pas | Relancer `securityadmin.sh` |

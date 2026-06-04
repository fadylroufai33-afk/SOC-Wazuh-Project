# 🚨 Exemples d'alertes détectées

## Résumé des alertes

| Date | Rule ID | Description | Niveau | Agent |
|---|---|---|---|---|
| 25 Avr 2026 | 5763 | SSH Brute Force | 10 — CRITIQUE | wazuh-VirtualBox |
| 25 Avr 2026 | 5760 | SSH Auth Failed | 5 — MOYEN | wazuh-VirtualBox |
| 11 Mai 2026 | 60106 | Windows Logon Success | 3 — BAS | windows-target |
| 11 Mai 2026 | 52002 | AppArmor DENIED | 3 — BAS | fadyl-HP-Laptop |
| 11 Mai 2026 | 504 | Agent disconnected | 3 — BAS | windows-target |
| 12 Mai 2026 | 5760 | SSH Auth Failed | 5 — MOYEN | wazuh-VirtualBox |

---

## Alerte 1 — SSH Brute Force (CRITIQUE)

**Rule 5763 — Niveau 10**

```
predecoder.hostname: wazuh-VirtualBox
data.srcip: 172.20.10.12
data.dstuser: root
rule.description: sshd: brute force trying to get access to the system
rule.mitre.id: T1110
rule.mitre.tactic: Credential Access
```

**Explication :** Le laptop de Fadyl (172.20.10.12) a tenté plusieurs mots de passe en séquence pour se connecter en SSH sur le serveur. Wazuh a détecté l'attaque en moins de 60 secondes.

---

## Alerte 2 — Ajout au groupe Administrateurs Windows

**Rule 4732 — Niveau élevé**

```
agent.name: windows-target
data.win.eventdata.targetUserName: Administrateurs
data.win.system.computer: Florine-Brie
rule.description: A member was added to a security-enabled local group
rule.mitre.tactic: Privilege Escalation
```

**Explication :** Un utilisateur a été ajouté au groupe Administrateurs sur la machine Windows. Action sensible détectée et enregistrée.

---

## Alerte 3 — AppArmor DENIED

**Rule 52002 — Niveau 3**

```
agent.name: fadyl-HP-Laptop-14-ep0xxx
data.status: DENIED
data.extra_data: ptrace
rule.description: Apparmor DENIED
```

**Explication :** Le navigateur Opera a tenté d'accéder à des fichiers système protégés. AppArmor (sécurité Linux) a bloqué l'accès.

---

## Alerte 4 — Agent déconnecté

**Rule 504 — Niveau 3**

```
agent.name: windows-target
rule.description: Wazuh agent disconnected
rule.mitre.id: T1562.001
rule.mitre.tactic: Defense Evasion
```

**Explication :** L'agent Windows s'est déconnecté du manager. Wazuh l'a immédiatement détecté et enregistré.

---

## Statistiques globales

- **Total alertes** : 20 000+
- **Alertes critiques (niveau 10+)** : 2
- **Alertes hautes (niveau 7-11)** : 8
- **Alertes moyennes (niveau 5-6)** : 244+
- **Agents surveillés** : 3
- **Période** : 24 Avril — 12 Mai 2026

# ✈️ Projet Stratégique ANAC
## Sécurité • Efficacité • Expérience Passager

**Bienvenue** dans le dépôt GitHub du **Projet Stratégique pour l’Aviation Civile au Togo**, développé en collaboration avec **ANAC (Agence Nationale de l'Aviation Civile)**.

Ce projet modernise les opérations aéronautiques en intégrant deux piliers technologiques :
- 🌤️ **IA pour la Météo** — Prévision ultra-précise des phénomènes dangereux pour l'ATM.
- 🎒 **Traçabilité Numérique des Bagages** — Solution basée sur QR Code pour éliminer les pertes et améliorer l'expérience passager.

---

## Table des matières
1. [Objectifs](#objectifs)
2. [Stack Technique](#stack-technique)
3. [Démarrage Rapide](#démarrage-rapide-mode-développement)
4. [Traçabilité des Bagages](#traçabilité-des-bagages-focus)
5. [Météo IA](#météo-ia-focus)
6. [Feuille de route (V2)](#feuille-de-route-v2)
7. [Contribution](#contribution)
8. [Crédits](#crédits)

---

## 🎯 Objectifs

Le système intégré (Fullstack AI) adresse deux problématiques critiques :

| Problématique | Objectif Principal | Solution Technologique |
|---:|:---|:---|
| **Sécurité / ATM** | Améliorer la prise de décision ATC face à la météo critique (turbulence, givrage, vents traversiers) | Modèles IA météo (GraphCast, Pangu-Weather) exposés via **FastAPI** |
| **Expérience Passager** | Réduire les pertes et retards de bagages, fournir transparence au passager | **QR Code** + PostgreSQL + API **Express.js** |

---

## 🛠️ Stack Technique

Architecture micro-services Fullstack :


**Composants :**
- **Frontend** : ReactJS — Console ATC et Interface de suivi passager (bagages).
- **Backend** : Express.js (Node.js) — Auth, gestion utilisateurs, endpoints bagages.
- **Microservice IA** : FastAPI (Python) — Inference GraphCast/Pangu-Weather + post-traitement.
- **DB** : PostgreSQL — Logs de scans + prédictions météo.
- **Conteneurisation** : Docker / Docker Compose.

---

## 🚀 Démarrage Rapide (Mode Développement)

### Prérequis
- Node.js (LTS)
- Python 3.10+
- Docker & Docker Compose

### 1) Cloner le dépôt
```bash
git clone https://github.com/votre-utilisateur/projet-anac-aviation.git
cd projet-anac-aviation

```
### 2) créer un fichier .env à le racine

# .env - Configuration d'exemple

# --- POSTGRESQL ---
DB_HOST=db_pg
DB_PORT=5432
DB_USER=anac_user
DB_PASSWORD=secret_password
DB_NAME=anac_db

# --- JWT / AUTH ---
JWT_SECRET_KEY=votre_cle_secrete_jwt

# --- Autres (exemples) ---
FRONTEND_PORT=3000
BACKEND_PORT=8080
IA_PORT=8000


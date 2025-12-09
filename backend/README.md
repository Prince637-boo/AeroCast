# ✈️ AeroCast – Backend (Microservices)

Bienvenue sur le backend de **AeroCast**, une plateforme aéronautique intelligente dédiée à la **météorologie aérienne en temps réel** et à la **traçabilité avancée des bagages**.

Ce projet est basé sur une **architecture microservices moderne** orientée haute performance, observabilité et scalabilité.

---

## 🏗️ Architecture Générale

AeroCast est construit autour de plusieurs microservices **FastAPI**, chacun étant responsable d’un domaine métier précis.

### Microservices Actuels

| Service | Rôle |
|--------|------|
| `auth-service` | Authentification, gestion des utilisateurs, RBAC |
| `baggage-service` | Traçabilité des bagages (QR, RFID, GPS, ADS-B ready) |
| `weather-service` | Données météo temps réel + mise à jour automatique |
| `worker-service` | Consommateurs RabbitMQ et tâches asynchrones |

---

## ⚙️ Stack Technique

### Framework & Langage
- **FastAPI**
- **Python 3.11+**
- **Asyncio**

### Base de données
- **PostgreSQL 16**
- **SQLAlchemy 2.0 (Async)**
- **Alembic (migrations)**

### Messaging & Temps réel
- **RabbitMQ** (broker de messages)
- **Redis** (cache + Pub/Sub temps réel)
- **WebSockets** (FastAPI)

### Observabilité & Monitoring
- **OpenTelemetry (OTEL)**
- **Jaeger (traces)**
- **Prometheus (metrics)**
- **ELK Stack**
  - Elasticsearch
  - Logstash
  - Kibana

### Stockage
- **MinIO (S3 Compatible)**

### Conteneurisation & Infra
- **Docker**
- **Docker Compose**
- **Traefik (Reverse Proxy + Gateway API)**
- **uv (gestion ultra-performante des dépendances)**

---

## 📁 Structure du Projet

backend/
├── services/
│ ├── auth/
│ ├── baggage/
│ ├── weather/
│ └── workers/
├── libs/
│ └── common/
├── docker/
│ └── entrypoint.sh
├── docker-compose.yml
├── otel-collector-config.yaml
└── prometheus.yml


---

## 🚀 Démarrage rapide

### Prérequis

- Docker / Docker Compose
- uv
- Python 3.11+
- PostgreSQL client (optionnel)
- Un fichier `.env`

---

### 1. Créer le fichier `.env`

```bash
cp .env.example .env
```

### 2. Lancer la stack complète

```bash
docker compose up --build
```

### 3. Lancer un seul service

Exemple : service auth uniquement

```bash
docker compose up auth
```

### 🧪 Tests

Les tests sont faits avec Pytest.

```bash
pytest
```


## 📖 Documentation interne

Chaque microservice expose sa documentation automatique FastAPI :

Auth	http://localhost:8001/docs
Bagages http://localhost:8002/docs
Météo   http://localhost:8003/docs

## 📡 Observabilité

Jaeger (Traces)
http://localhost:16686

Prometheus (Metrics)
http://localhost:9090

Kibana (Logs)
http://localhost:5601


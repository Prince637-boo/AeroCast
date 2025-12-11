# AeroCast – Backend (Microservices)

Bienvenue sur le backend de AeroCast, une plateforme aéronautique dédiée à la météorologie aérienne en temps réel et à la traçabilité avancée des bagages.

Le projet est basé sur une architecture microservices orientée haute performance, observabilité et scalabilité.

## Architecture générale

AeroCast est construit autour de plusieurs microservices FastAPI, chacun responsable d’un domaine métier spécifique.

### Microservices actuels

| Service     | Rôle                                                        |
|-------------|-------------------------------------------------------------|
| [auth](./services/auth)        | Authentification, gestion des utilisateurs, RBAC            |
| [baggage](./services/baggage)  | Traçabilité des bagages (QR, RFID, GPS, ADS‑B ready)        |
| [weather](./services/weather)  | Données météo en temps réel et prévisions                   |
| [orientation](./services/orientation) | Orientation des passagers selon bagages, vol et météo      |

Chaque service fonctionne de manière indépendante, et peut être couplé via Redis Pub/Sub et RabbitMQ pour un écosystème temps réel.

## Stack technique

- Framework & langage
    - FastAPI
    - Python 3.11+
    - asyncio
- Base de données
    - PostgreSQL 16
    - SQLAlchemy 2.0 (Async)
    - Alembic (migrations)
- Messaging & temps réel
    - RabbitMQ (broker)
    - Redis (cache + Pub/Sub)
    - WebSockets (FastAPI)
- Observabilité & monitoring
    - OpenTelemetry (OTEL)
    - Jaeger (traces)
    - Prometheus (metrics)
    - ELK (Elasticsearch, Logstash, Kibana)
- Stockage
    - MinIO (S3 compatible)
- Conteneurisation & infra
    - Docker, Docker Compose
    - Traefik (reverse proxy / API gateway)
    - uv (gestion des dépendances)

## Démarrage rapide

### Prérequis
- Docker / Docker Compose
- uv (gestion des dépendances)
- Python 3.11+
- Client PostgreSQL (optionnel)
- Fichier `.env`

### 1. Créer le fichier .env
```bash
cp .env.example .env
```
Configurer les variables d’environnement (PostgreSQL, Redis, RabbitMQ, clés API, etc.).

### 2. Lancer la stack complète
```bash
docker compose up --build
```

### 3. Lancer un seul service
Exemple : lancer uniquement le service `auth`
```bash
docker compose up auth
```

### 4. Lancer en local sans Docker
Se placer dans le dossier /backend/:
```bash
python -m uvicorn services.<nom_service>.main:app --reload --port <port>
```
Exemple pour le service météo :
```bash
python -m uvicorn services.weather.main:app --reload --port 8003
```

## Tests

Les tests utilisent pytest :
```bash
pytest
```
Chaque microservice contient un dossier `tests/` dédié.

## Documentation interne (Swagger)

Chaque microservice expose sa documentation FastAPI automatiquement.

| Service   | URL docs                      |
|-----------|-------------------------------|
| Auth      | [http://localhost:8001/docs](http://localhost:8001/docs)    |
| Bagages   | [http://localhost:8002/docs](http://localhost:8002/docs)    |
| Météo     | [http://localhost:8003/docs](http://localhost:8003/docs)    |
| Orientation | [http://localhost:8004/docs](http://localhost:8004/docs)  |

## Observabilité

- Jaeger (traces) : [http://localhost:16686](http://localhost:16686)  
- Prometheus (metrics) : [http://localhost:9090](http://localhost:9090)  
- Kibana (logs) : [http://localhost:5601](http://localhost:5601)

## Notes importantes

- Les microservices sont modulaires et peuvent être déployés indépendamment.
- Interaction temps réel via Redis Pub/Sub ; messages asynchrones via RabbitMQ.
- `uv` permet une installation rapide et un démarrage simplifié en développement.
- Adapter les variables d’environnement et les ports selon votre environnement.


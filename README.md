# ✈️ Guide Intelligent Passager (GIP) : Maîtrisez le Destin du Voyageur

Le **GIP** (Guide Intelligent Passager) est le Projet Stratégique pour l'Aviation Civile au Togo, développé en collaboration avec l'**ANAC (Agence Nationale de l'Aviation Civile)**.

Ce dépôt contient le cœur de la plateforme, surnommé **AeroCast**, qui met en œuvre une architecture microservices orientée haute performance, observabilité et scalabilité. Notre mission est de transformer l'expérience aéroportuaire en intégrant l'IA pour la sécurité opérationnelle et la traçabilité numérique pour la sûreté et l'expérience passager.

---

> 
> Toutes les fonctionnalités de base (IA Météo, Traçabilité Bagages, Microservices) ont été **développées et validées unitairement**. Le code des services backend est complet.
> 
> Les systèmes sont actuellement en cours d'intégration dans l'environnement conteneurisé complet (Docker Compose) pour les tests finaux et le déploiement. **Le code est prêt, l'infrastructure est en cours de finalisation.**
> 
> ---

## 🎯 Vision et Piliers Stratégiques

Le GIP se fonde sur la résilience opérationnelle à travers trois piliers technologiques essentiels :

| Pilier | Problème Adressé | Objectif (ROI) | Solution Technologique |
| :--- | :--- | :--- | :--- |
| **1. Intelligence (IA) - *Safety*** | Imprévisibilité de la météo | Sécurité Opérationnelle Maximale | Prévention des risques (ex: cisaillement de vent) **45 min avant** l'impact. |
| **2. Orientation Dynamique - *Fluidité*** | Chaos logistique & passagers perdus | Réduction de la congestion & **Just-In-Time Boarding** | Guidage instantané et instructions personnalisées pour désengorger les zones critiques. |
| **3. Preuve (Traçabilité) - *Security*** | Bagages égarés et risques de sûreté | Transparence totale, élimination du stress passager | Suivi de bagages de bout en bout (QR/RFID + GPS). |

> **Notre philosophie :** L'anticipation n'est pas une simple information, mais une instruction directe et précise pour le passager.

---

## 🛠️ Fonctionnalités Clés du GIP

### 1. Expérience Passager (Interface Mobile - Frontend)

* **Alerte Proactive :** Messages personnalisés basés sur l'IA (ex: "Allez vers Porte F12. Évitez la zone B").
* **Guidage Adaptatif :** Navigation en temps réel qui réagit aux incidents (météo, congestion, changement de porte) et recalcule les chemins.
* **Suivi Bagages (Transparence Totale) :** Timeline verticale montrant le statut du bagage de l'enregistrement au chargement.

### 2. Interface Opérationnelle (ANAC Admin - Frontend/Backend)

* **ZONES DE DENSITÉ :** Visualisation en temps réel des zones de congestion pour une gestion proactive des flux.
* **Centre de Gestion des Alertes :** Tableau de bord pour les alertes (Météo, Sécurité, Logistique) avec statut (ENVOYÉ, ACTION REQUISE, PROGRAMMÉ).
* **Alertes Prédictives :** Avertissement sur les risques de saturation du terminal avant qu'ils ne surviennent.

---

# GIP – Backend : Architecture Microservices (AeroCast)

Ce répertoire contient l'ensemble des microservices Python/FastAPI qui constituent le cœur du GIP. L'architecture est conçue pour être modulaire et résiliente.



[Image of Microservices Architecture Diagram]


## Architecture générale

AeroCast est construit autour de plusieurs microservices FastAPI, chacun responsable d’un domaine métier spécifique.

### Microservices actuels

| Service | Rôle | Port Interne |
| :--- | :--- | :--- |
| [auth](./services/auth) | Authentification, gestion des utilisateurs, RBAC | 8001 |
| [baggage](./services/baggage) | Traçabilité des bagages (QR, RFID, GPS, ADS‑B ready) | 8002 |
| [weather](./services/weather) | Données météo en temps réel et prévisions (API Open Météo + IA) | 8003 |
| [orientation](./services/orientation) | Orientation des passagers selon bagages, vol et météo | 8004 |

> Chaque service fonctionne de manière indépendante, utilisant Redis Pub/Sub pour la communication en temps réel et RabbitMQ pour les tâches asynchrones et la gestion des événements.

## ⚙️ Stack Technique détaillée

| Catégorie | Technologie(s) | Notes |
| :--- | :--- | :--- |
| **Framework & Langage** | FastAPI, Python 3.11+, asyncio | Hautes performances et documentation automatique. |
| **Base de Données** | PostgreSQL 16, SQLAlchemy 2.0 (Async), Alembic | Base de données principale avec ORM asynchrone et migrations. |
| **Messaging & Temps Réel** | RabbitMQ (broker), Redis (cache + Pub/Sub), WebSockets | Gestion des événements asynchrones et des communications instantanées. |
| **Observabilité & Monitoring** | OpenTelemetry (OTEL), Jaeger, Prometheus, ELK (Elasticsearch, Logstash, Kibana) | Traces distribuées, métriques et gestion des logs centralisée. **Crucial pour la résilience.** |
| **Stockage** | MinIO (S3 compatible) | Stockage d'objets (ex: données brutes météo, images de profil). |
| **Conteneurisation & Infra** | Docker, Docker Compose, Traefik, uv | Environnement reproductible, API Gateway et gestion des dépendances simplifiée. |

### 🌤️ Note Spécifique sur l'IA Météo

Le service `weather` utilise les données Open Météo, mais la structure est prête pour l'intégration des modèles de Machine Learning avancés. Les travaux de recherche pour l'implémentation de **GraphCast** sont disponibles sur le notebook Colab suivant :
[https://colab.research.google.com/drive/1BgAz1iIPkcA_u2weOpEG6reLnJxwSlA_?usp=sharing](https://colab.research.google.com/drive/1BgAz1iIPkcA_u2weOpEG6reLnJxwSlA_?usp=sharing)

---

## 🚀 Démarrage Rapide

### Prérequis
- Docker / Docker Compose
- `uv` (gestion des dépendances Python, recommandé)
- Python 3.11+
- Fichier `.env`

### 1. Clonage du Dépôt

```bash
git clone [https://github.com/Prince637-boo/GIP.git](https://github.com/Prince637-boo/GIP.git)
cd AeroCast
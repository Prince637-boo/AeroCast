#!/bin/bash
# Script d'initialisation complète du projet ANAC

set -e  # Arrêter en cas d'erreur

echo "🚀 Initialisation du projet ANAC Aviation Platform..."

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# 1. CRÉER LA STRUCTURE DES DOSSIERS
# ============================================================================
echo -e "${BLUE}📁 Création de la structure des dossiers...${NC}"

# Service Auth
cd Aerocast_BackEnd/app/api/service_auth_api
mkdir -p {models,schemas,services,utils,core,db}
mkdir -p routes/{auth,utilisateurs,admin}
touch models/__init__.py schemas/__init__.py services/__init__.py utils/__init__.py
touch core/__init__.py db/__init__.py routes/__init__.py
touch routes/auth/__init__.py routes/utilisateurs/__init__.py routes/admin/__init__.py
cd ../../../../

# Service Bagages
cd Aerocast_BackEnd/app/api/service_baggages_api
mkdir -p {models,schemas,services,utils,core,db,websockets}
mkdir -p routes/{bagages,qr,admin}
touch models/__init__.py schemas/__init__.py services/__init__.py utils/__init__.py
touch core/__init__.py db/__init__.py routes/__init__.py websockets/__init__.py
touch routes/bagages/__init__.py routes/qr/__init__.py routes/admin/__init__.py
cd ../../../../

# Service Météo IA
cd Aerocast_BackEnd/app/api/service_meteo_ia_api
mkdir -p {models,schemas,services,utils,core,db,ml}
mkdir -p routes/{meteo,aeroports,admin}
mkdir -p models_ai  # Pour stocker les modèles IA
touch models/__init__.py schemas/__init__.py services/__init__.py utils/__init__.py
touch core/__init__.py db/__init__.py routes/__init__.py ml/__init__.py
touch routes/meteo/__init__.py routes/aeroports/__init__.py routes/admin/__init__.py
cd ../../../../

echo -e "${GREEN}✅ Structure des dossiers créée !${NC}"

# ============================================================================
# 2. COPIER LES FICHIERS DE CONFIGURATION
# ============================================================================
echo -e "${BLUE}📝 Copie des fichiers de configuration...${NC}"

# Copier core/config.py dans chaque service
for service in service_auth_api service_baggages_api service_meteo_ia_api; do
    cp Aerocast_BackEnd/app/core/config.py Aerocast_BackEnd/app/api/$service/core/
    cp Aerocast_BackEnd/app/core/security.py Aerocast_BackEnd/app/api/$service/core/
done

echo -e "${GREEN}✅ Fichiers de configuration copiés !${NC}"

# ============================================================================
# 3. INITIALISER UV ET INSTALLER LES DÉPENDANCES
# ============================================================================
echo -e "${BLUE}📦 Installation des dépendances avec UV...${NC}"

for service in service_auth_api service_baggages_api service_meteo_ia_api; do
    echo -e "${YELLOW}  → Installation pour $service${NC}"
    cd Aerocast_BackEnd/app/api/$service
    
    # Si uv.lock n'existe pas, l'initialiser
    if [ ! -f "uv.lock" ]; then
        uv lock
    fi
    
    # Installer les dépendances
    uv sync
    
    cd ../../../../
done

echo -e "${GREEN}✅ Dépendances installées !${NC}"

# ============================================================================
# 4. CRÉER LE FICHIER .env.dev SI IL N'EXISTE PAS
# ============================================================================
if [ ! -f ".env.dev" ]; then
    echo -e "${BLUE}🔐 Création du fichier .env.dev...${NC}"
    cat > .env.dev <<'EOF'
# Configuration ANAC
PROJECT_NAME=AEROCAST
PROJECT_VERSION=1.0.0
API_V1_STR=/api/v1

# Base de données
POSTGRES_USER=postgres
POSTGRES_PASSWORD=Ch4ng3M3!
POSTGRES_DB=anac_aviation
DATABASE_URL=postgresql://postgres:Ch4ng3M3!@db:5432/anac_aviation

# Sécurité
SECRET_KEY=79c01c0a30c2ee15f409287aac2d913f02c58b2ee60b06f274cc109dab5a1426
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin par défaut
FIRST_SUPERUSER=admin@anac.tg
FIRST_SUPERUSER_PASSWORD=AdminPassword123!
FIRST_SUPERUSER_NOM=Administrateur ANAC

# Ports
PORT_AUTH=8001
PORT_BAGAGES=8002
PORT_METEO=8003

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# RabbitMQ
RABBITMQ_USER=guest
RABBITMQ_PASS=guest

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:80

# Debug
DEBUG=true
LOG_LEVEL=INFO
EOF
    echo -e "${GREEN}✅ Fichier .env.dev créé !${NC}"
else
    echo -e "${YELLOW}⚠️  .env.dev existe déjà, pas de modification.${NC}"
fi

# ============================================================================
# 5. VÉRIFIER QUE DOCKER EST INSTALLÉ
# ============================================================================
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker n'est pas installé. Installez-le avant de continuer.${NC}"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose n'est pas installé. Installez-le avant de continuer.${NC}"
    exit 1
fi

# ============================================================================
# 6. AFFICHER LES PROCHAINES ÉTAPES
# ============================================================================
echo ""
echo -e "${GREEN}=====================================================================${NC}"
echo -e "${GREEN}✅ Initialisation terminée avec succès !${NC}"
echo -e "${GREEN}=====================================================================${NC}"
echo ""
echo -e "${BLUE}📋 Prochaines étapes :${NC}"
echo ""
echo "1. Lancer les services Docker :"
echo -e "   ${YELLOW}docker-compose up -d${NC}"
echo ""
echo "2. Vérifier les logs :"
echo -e "   ${YELLOW}docker-compose logs -f${NC}"
echo ""
echo "3. Tester les services :"
echo -e "   ${YELLOW}curl http://localhost/health${NC}"
echo -e "   ${YELLOW}curl http://localhost:8001/health  # Service Auth${NC}"
echo -e "   ${YELLOW}curl http://localhost:8002/health  # Service Bagages${NC}"
echo -e "   ${YELLOW}curl http://localhost:8003/health  # Service Météo${NC}"
echo ""
echo "4. Accéder à la documentation API :"
echo -e "   ${YELLOW}http://localhost:8001/docs  # Swagger Auth${NC}"
echo ""
echo "5. Créer le premier utilisateur admin :"
echo -e "   ${YELLOW}python scripts/create_admin.py${NC}"
echo ""
echo -e "${GREEN}=====================================================================${NC}"
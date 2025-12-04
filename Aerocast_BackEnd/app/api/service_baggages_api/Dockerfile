FROM ghcr.io/astral-sh/uv:python3.11-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Installer uv
RUN pip install uv

# Copier les fichiers de dépendances
COPY uv.lock pyproject.toml ./

# Installer les dépendances avec uv
RUN uv sync --frozen

# Copier le reste du code
COPY . .

EXPOSE 8000

# Lancer l'application FastAPI avec uvicorn via uv
CMD ["uv", "run", "--", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

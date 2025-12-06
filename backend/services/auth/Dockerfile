FROM python:3.11 

ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY libs ./libs
COPY services/auth ./services/auth

RUN uv pip install --system --no-cache -e .

EXPOSE 8000

CMD ["uvicorn", "services.auth.main:app", "--host", "0.0.0.0", "--port", "8000"]
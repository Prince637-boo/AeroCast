FROM python:3.11

ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY libs ./libs
COPY services/weather ./services/weather

RUN uv pip install --system --no-cache -e .

RUN mkdir -p /app/models

EXPOSE 8002

CMD ["uvicorn", "services.weather.main:app", "--host", "0.0.0.0", "--port", "8002"]
```

from fastapi import APIRouter, WebSocket
import asyncio
import redis.asyncio as redis

router = APIRouter(prefix="/ws/baggages")

@router.websocket("/stream")
async def baggage_stream(ws: WebSocket):
    """
    WebSocket pour recevoir en temps réel les événements liés aux bagages.

    Événements écoutés depuis Redis :
    - "baggage.scan" : lorsqu'un bagage est scanné
    - "baggage.status" : lorsqu'un bagage change de statut

    Frontend peut se connecter sur : ws://<host>/ws/baggages/stream
    """
    await ws.accept()
    print("WebSocket connection accepted")

    # -------------------------------
    # Connexion Redis
    # -------------------------------
    redis_client = redis.Redis(
        host="localhost",  # ou settings.REDIS_HOST
        port=6379,         # ou settings.REDIS_PORT
        decode_responses=True
    )

    pubsub = redis_client.pubsub()
    await pubsub.subscribe("baggage.scan", "baggage.status")
    print("Subscribed to Redis channels: baggage.scan, baggage.status")

    try:
        while True:
            # Récupération des messages Redis
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and "data" in message:
                await ws.send_text(message["data"])
            await asyncio.sleep(0.01)  # petite pause pour ne pas bloquer la boucle
    except Exception as e:
        print(f"WebSocket closed: {e}")
        await ws.close()
    finally:
        # Nettoyage : désabonnement et fermeture du client Redis
        await pubsub.unsubscribe("baggage.scan", "baggage.status")
        await redis_client.close()
        print("Redis connection closed and unsubscribed")

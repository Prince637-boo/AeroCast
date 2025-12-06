from fastapi import APIRouter, WebSocket
import asyncio
import redis.asyncio as redis

router = APIRouter(prefix="/ws/baggages")

@router.websocket("/stream")
async def baggage_stream(ws: WebSocket):
    await ws.accept()

    # Connexion Redis
    redis_client = redis.Redis(
        host="localhost",  # ou settings.REDIS_HOST
        port=6379,         # ou settings.REDIS_PORT
        decode_responses=True
    )

    pubsub = redis_client.pubsub()
    await pubsub.subscribe("baggage.scan", "baggage.status")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and "data" in message:
                await ws.send_text(message["data"])
            await asyncio.sleep(0.01)
    except Exception as e:
        print(f"WebSocket closed: {e}")
        await ws.close()
    finally:
        await pubsub.unsubscribe("baggage.scan", "baggage.status")
        await redis_client.close()

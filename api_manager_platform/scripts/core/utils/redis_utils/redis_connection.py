import redis.asyncio as redis
from scripts.constants.app_configuration import settings

redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    ssl=True
)

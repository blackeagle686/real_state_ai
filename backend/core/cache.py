import redis.asyncio as redis
import hashlib
from backend.core.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=False
        )

    def _generate_key(self, text: str, voice_id: str) -> str:
        """Generates a unique key for the text + voice combination."""
        combined = f"{text}:{voice_id}"
        return hashlib.sha256(combined.encode()).hexdigest()

    async def get_audio(self, text: str, voice_id: str) -> bytes | None:
        """Retrieves cached audio for the given text."""
        key = self._generate_key(text, voice_id)
        return await self.redis_client.get(key)

    async def set_audio(self, text: str, voice_id: str, audio_data: bytes, expire: int = 86400):
        """Caches audio data for the given text."""
        key = self._generate_key(text, voice_id)
        await self.redis_client.set(key, audio_data, ex=expire)

cache_service = CacheService()

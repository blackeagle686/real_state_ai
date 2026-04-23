import httpx
from core.config import settings
from typing import AsyncGenerator

from core.cache import cache_service
from utils.logger import logger

class ElevenLabsService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1"
        self.voice_id = "pNInz6obpgDQGcFmaJgB"

    async def stream_tts(self, text: str) -> AsyncGenerator[bytes, None]:
        """
        Streams audio chunks from ElevenLabs API with Redis caching.
        """
        # Check cache first
        cached_audio = await cache_service.get_audio(text, self.voice_id)
        if cached_audio:
            logger.info(f"Cache hit for text: {text[:20]}...")
            yield cached_audio
            return

        logger.info(f"Cache miss for text: {text[:20]}...")
        url = f"{self.base_url}/text-to-speech/{self.voice_id}/stream"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "accept": "audio/mpeg"
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }

        audio_buffer = bytearray()
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", url, headers=headers, json=data) as response:
                    if response.status_code != 200:
                        logger.error(f"ElevenLabs error: {response.status_code}")
                        yield b""
                        return

                    async for chunk in response.aiter_bytes():
                        audio_buffer.extend(chunk)
                        yield chunk
                
                # Cache the accumulated audio
                if audio_buffer:
                    await cache_service.set_audio(text, self.voice_id, bytes(audio_buffer))
            except Exception as e:
                logger.error(f"TTS stream error: {e}")
                yield b""

tts_service = ElevenLabsService()

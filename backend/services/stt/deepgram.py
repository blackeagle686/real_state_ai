import json
import asyncio
from deepgram import Deepgram
from backend.core.config import settings

class STTService:
    def __init__(self):
        self.dg_client = Deepgram(settings.DEEPGRAM_API_KEY)

    async def get_streaming_connection(self, callback):
        """
        Establishes a streaming connection to Deepgram.
        """
        options = {
            "punctuate": True,
            "language": "ar",
            "model": "nova-2",
            "interim_results": True,
        }
        
        try:
            connection = await self.dg_client.transcription.live(options)
            
            # Set up listeners
            connection.register_handler(
                connection.event.CLOSE,
                lambda c: print(f"Deepgram connection closed: {c}")
            )
            connection.register_handler(
                connection.event.TRANSCRIPT_RECEIVED,
                lambda message: callback(message)
            )
            
            return connection
        except Exception as e:
            print(f"Failed to connect to Deepgram: {e}")
            return None

stt_service = STTService()

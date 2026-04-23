import json
import asyncio
from deepgram import (
    DeepgramClient,
    LiveOptions,
    LiveTranscriptionEvents,
)
from core.config import settings

class STTService:
    def __init__(self):
        self.dg_client = DeepgramClient(settings.DEEPGRAM_API_KEY)

    async def get_streaming_connection(self, callback):
        """
        Establishes a streaming connection to Deepgram (v3 syntax).
        """
        try:
            dg_connection = self.dg_client.listen.live.v("1")
            
            options = LiveOptions(
                punctuate=True,
                language="ar",
                model="nova-2",
                interim_results=True,
            )

            # Set up listeners
            dg_connection.on(LiveTranscriptionEvents.Close, lambda self, close, **kwargs: print(f"Deepgram connection closed: {close}"))
            dg_connection.on(LiveTranscriptionEvents.Transcript, lambda self, result, **kwargs: callback(result.to_dict()))
            
            # Start the connection
            if dg_connection.start(options) is False:
                print("Failed to start Deepgram connection")
                return None
            
            return dg_connection
        except Exception as e:
            print(f"Failed to connect to Deepgram: {e}")
            return None

stt_service = STTService()

import asyncio
from typing import AsyncGenerator
from services.llm.longcat import llm_service
from services.tts.elevenlabs import tts_service
from utils.token_buffer import TokenBuffer

class PipelineCoordinator:
    def __init__(self):
        self.token_buffer = TokenBuffer(min_words=10, max_words=20)
        self.current_tts_task = None

    async def process_text_stream(self, text_input: str) -> AsyncGenerator[bytes, None]:
        """
        Takes text input (from STT), streams from LLM, buffers, and yields audio chunks.
        """
        async for token in llm_service.stream_response(text_input):
            chunk = await self.token_buffer.add_token(token)
            if chunk:
                async for audio_chunk in tts_service.stream_tts(chunk):
                    yield audio_chunk
        
        # Flush the buffer at the end
        final_chunk = self.token_buffer.flush()
        if final_chunk:
            async for audio_chunk in tts_service.stream_tts(final_chunk):
                yield audio_chunk

pipeline_coordinator = PipelineCoordinator()

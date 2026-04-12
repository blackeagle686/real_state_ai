import openai
from backend.core.config import settings

class LLMService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=settings.LONGCAT_API_KEY,
            base_url=settings.LONGCAT_BASE_URL
        )

    async def generate_response(self, prompt: str, history: list = None):
        if history is None:
            history = []
        
        messages = history + [{"role": "user", "content": prompt}]
        
        response = await self.client.chat.completions.create(
            model="longcat-model",
            messages=messages,
            stream=False
        )
        
        return response.choices[0].message.content

    async def stream_response(self, prompt: str, history: list = None):
        if history is None:
            history = []
        
        messages = history + [{"role": "user", "content": prompt}]
        
        stream = await self.client.chat.completions.create(
            model="longcat-model",
            messages=messages,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

llm_service = LLMService()

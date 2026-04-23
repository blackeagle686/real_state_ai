from IRYM_sdk import ChatBot
from typing import Optional

class RealEstateChatbot:
    def __init__(self):
        self.bot = None

    async def initialize(self):
        # Configure ChatBot to use OpenAI (Long Cat) and RAG
        # We pass local=False to ensure it doesn't try to load local weights
        self.bot = (ChatBot(local=False, vlm=False)
               .with_rag(["./data"])
               .with_memory()
               .with_system_prompt(
                   "You are an expert Real Estate Assistant for Saudi Arabia. "
                   "You provide detailed information about land and apartment prices, "
                   "rank properties based on user criteria (price, location, rating), "
                   "and give professional investment recommendations. "
                   "Always cite your sources from the provided data."
               )
               .build())
        print("[+] Real Estate Chatbot initialized with Long Cat and RAG.")

    async def chat(self, message: str, session_id: Optional[str] = None):
        if not self.bot:
            await self.initialize()
            
        if session_id:
            self.bot.set_session(session_id)
            
        response = await self.bot.chat(message)
        return response

real_estate_chatbot = RealEstateChatbot()

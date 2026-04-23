from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.core.config import settings
from backend.services.llm.longcat import llm_service
from backend.services.tts.gtts_service import tts_service
from backend.websocket.voice import router as voice_router
from backend.services.chatbot_service import real_estate_chatbot
from IRYM_sdk import init_irym, startup_irym
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

@app.on_event("startup")
async def startup_event():
    print("[*] Initializing IRYM Infrastructure...")
    init_irym()
    await startup_irym()
    await real_estate_chatbot.initialize()
    print("[+] System Ready.")

app.include_router(voice_router)

# Setup Static Files and Templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "project_name": settings.PROJECT_NAME})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat")
async def chat_with_assistant(request: dict):
    message = request.get("message", "")
    session_id = request.get("session_id", "default_user")
    
    if not message:
        return {"error": "Message is required"}
        
    response = await real_estate_chatbot.chat(message, session_id=session_id)
    return {"response": response}

@app.post("/api/voice/generate")
async def generate_voice(request: dict):
    text = request.get("text", "مرحباً")
    # In Phase 1, we might just use the text directly or via LLM
    # Let's say we use LLM first
    # response_text = await llm_service.generate_response(text)
    # For now, just gTTS the input text for speed of test
    audio_data = await tts_service.text_to_speech(text)
    return Response(content=audio_data, media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

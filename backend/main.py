from fastapi import FastAPI, Response
from backend.core.config import settings
from backend.services.llm.longcat import llm_service
from backend.services.tts.gtts_service import tts_service
from backend.websocket.voice import router as voice_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(voice_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

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

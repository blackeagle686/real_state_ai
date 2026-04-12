import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.stt.deepgram import stt_service
from backend.services.pipeline import pipeline_coordinator

router = APIRouter()

@router.websocket("/ws/voice-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Queue for transcripts from STT to LLM
    transcript_queue = asyncio.Queue()
    
    # Task to handle STT callbacks
    def stt_callback(message):
        transcript = message.get("channel", {}).get("alternatives", [{}])[0].get("transcript", "")
        is_final = message.get("is_final", False)
        if transcript and is_final:
            asyncio.create_task(transcript_queue.put(transcript))

    dg_connection = await stt_service.get_streaming_connection(stt_callback)
    if not dg_connection:
        await websocket.close(code=1011)
        return

    # Variable to keep track of current processing task
    processing_task = None

    # Task to process transcripts and send audio back
    async def process_and_send():
        nonlocal processing_task
        try:
            while True:
                transcript = await transcript_queue.get()
                
                # If a task is already running, cancel it (Interrupt Handling)
                if processing_task and not processing_task.done():
                    processing_task.cancel()
                    try:
                        await processing_task
                    except asyncio.CancelledError:
                        pass
                
                # Start new pipeline task
                processing_task = asyncio.create_task(run_pipeline(transcript))
        except Exception as e:
            print(f"Error in process_and_send: {e}")

    async def run_pipeline(transcript: str):
        try:
            async for audio_chunk in pipeline_coordinator.process_text_stream(transcript):
                await websocket.send_bytes(audio_chunk)
        except asyncio.CancelledError:
            # Handle cancellation gracefully
            pass
        except Exception as e:
            print(f"Error in run_pipeline: {e}")

    sender_manager_task = asyncio.create_task(process_and_send())

    try:
        while True:
            # Receive audio chunks from client
            data = await websocket.receive_bytes()
            dg_connection.send(data)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        sender_manager_task.cancel()
        if processing_task:
            processing_task.cancel()
        dg_connection.finish()
        await websocket.close()


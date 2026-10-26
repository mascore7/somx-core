from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from somx_core.engine import SovereignEngine
from somx_core.config import settings

app = FastAPI(title=settings.app_name, version="1.0.0")

# Bilow mashiinka wakiilada madaxa bannaan (Autonomous Agents Engine)
engine = SovereignEngine()

@app.get("/")
async def root():
    return {
        "status": "online",
        "ecosystem": settings.app_name,
        "environment": settings.environment
    }

@app.websocket("/ws/v1/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            prompt = data.get("prompt", "")
            
            # Si live ah u daadi jawaabaha mashiinka iyo RAG-ga
            async for response_chunk in engine.stream_agent_response(prompt):
                await websocket.send_text(response_chunk)
    except WebSocketDisconnect:
        # Xiritaanka xiriirka markuu isticmaalaha baxo
        pass

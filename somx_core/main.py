from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from somx_core.engine import SovereignEngine
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SOMX-Sovereign")

app = FastAPI(
    title="SOMX.NET Sovereign AI Engineering Ecosystem",
    version="1.0.0",
    description="Next-generation autonomous agentic AI streaming framework."
)

# Enable CORS for global/live accessibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SovereignEngine()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected: {websocket.client}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "online", "ecosystem": "SOMX.NET", "mode": "Live Sovereign"}

@app.websocket("/ws/v1/stream")
async def sovereign_websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive data payload from client
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            prompt = data.get("prompt", "Hello SOMX")

            # Stream responses back live token-by-token or chunk-by-chunk
            async for chunk in engine.stream_agent_response(prompt):
                await websocket.send_text(chunk)
                
            # Send completion signal
            await websocket.send_text(json.dumps({"status": "completed", "data": "[DONE]"}))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({"status": "info", "message": "A client disconnected."}))
    except Exception as e:
        logger.error(f"Error in WebSocket session: {str(e)}")
        await websocket.close(code=1011)

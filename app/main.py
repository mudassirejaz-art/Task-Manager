from fastapi import FastAPI, WebSocket, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.routers import tasks
from app.pubsub import PubSub, get_pubsub
import os
import json
from starlette.websockets import WebSocketState

app = FastAPI(title="Task Manager API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(tasks.router)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/health")
async def health_check():
    return {"message": "API is running 🚀"}

# WebSocket
@app.websocket("/ws/tasks")
async def ws_tasks(websocket: WebSocket, pubsub: PubSub = Depends(get_pubsub)):
    await websocket.accept()
    try:
        async for message in pubsub.subscribe("tasks"):
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_text(json.dumps(message))
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.close()
        except RuntimeError:
            pass

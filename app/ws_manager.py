import asyncio
from fastapi import WebSocket
from typing import Set
import json

class WSManager:
    def __init__(self):
        self._clients: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self._clients.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self._clients:
                self._clients.remove(websocket)
        try:
            await websocket.close()
        except Exception:
            pass

    async def broadcast(self, message: dict):
        data = json.dumps(message)
        async with self._lock:
            clients = list(self._clients)
        coros = []
        for ws in clients:
            coros.append(self._send_safe(ws, data))
        if coros:
            await asyncio.gather(*coros, return_exceptions=True)

    async def _send_safe(self, websocket: WebSocket, data: str):
        try:
            await websocket.send_text(data)
        except Exception:
            # if sending fails, try to remove client
            await self.disconnect(websocket)

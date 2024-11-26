import json
import asyncio
import os
import sys
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.logger = logging.getLogger(__name__)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info(f"Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logging.info(f"Client disconnected: {websocket.client}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            print("No active connections to broadcast to.")
            return
        data = json.dumps(message)
        for connection in self.active_connections:
            await connection.send_text(data)

manager = ConnectionManager()
environment = Enviroment()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            agents_data = environment.moveAll()
            await manager.broadcast(agents_data)
            await asyncio.sleep(1 / 60)  # 30 updates per second
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)
import json
import asyncio
import os
import random
import sys
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from Object import Object
from Food import Food
from Agent import Agent

from Enviroment import Enviroment
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
            return
        data = json.dumps(message)
        for connection in self.active_connections:
            await connection.send_text(data)

manager = ConnectionManager()
environment = Enviroment(1000, 1000, minCountAgent=80, minCountFood=200)

environment.spawnObjects(Food, 400, foodlevel=20)
environment.spawnObjects(Agent, 100)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubt den Zugriff von deinem Frontend
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubt alle HTTP-Methoden
    allow_headers=["*"],  # Erlaubt alle Header
)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Client {client_id} sent: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)

@app.get("/getObject/{id}")
async def getObject(id: int):
    objS = None
    for obj in environment.objects:
        if obj.id == id:
            objS = obj
    print(objS.collectInDetail())
    return objS.collectInDetail()

@app.get("/getENVSettings")
async def getENVSettings():
    return {"width": environment.width, "height": environment.height}

# start the server
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_environment())
    asyncio.create_task(broadcast_data())

async def update_environment():
    while True:
        environment.update()
        await asyncio.sleep(1 / 60)  # 60 updates per second

async def broadcast_data():
    while True:
        agents_data = environment.collectAll()
        await manager.broadcast(agents_data)
        await asyncio.sleep(1 / 60)

if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, app=app)


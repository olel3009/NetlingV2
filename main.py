import asyncio
import logging
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from Objects.Food import Food
from Objects.Agent import Agent
from Manager.EnvironmentManager import Enviroment
from Manager.NetworkManager import ConnectionManager

logging.basicConfig(level=logging.INFO)

manager = ConnectionManager()
environment = Enviroment(500, 500, minCountAgent=20, minCountFood=200)

environment.spawnObjectsInRect(Food, 40, foodlevel=20)
environment.spawnObjectsInRect(Agent, 5)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubt den Zugriff von deinem Frontend
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubt alle HTTP-Methoden
    allow_headers=["*"],  # Erlaubt alle Header
)

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Client sent: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logging.info("Client disconnected.")
    except Exception as e:
        logging.error(f"Error: {e}")
        manager.disconnect(websocket)

@app.get("/getObject/{id}")
async def getObject(id: int):
    objS = None
    for obj in environment.objects:
        if obj.id == id:
            objS = obj
    return objS.collectInDetail()

@app.get("/getENVSettings")
async def getENVSettings():
    return {"width": environment.width, "height": environment.height}

@app.get("/getBiome")
async def getBiome():
    biomeMap = environment.biomeManager.biomeInstanceMap.tolist()  # Convert to list of key-value pairs
    return {"map": biomeMap, "classes": [{"id": b.id, "name": b.__class__.__name__} for b in environment.biomeManager.biomeInstances]}

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

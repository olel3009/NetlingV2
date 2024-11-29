from typing import List

from fastapi import WebSocket, WebSocketDisconnect
import logging
import json
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info(f"Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logging.info(f"Client disconnected: {websocket.client}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        data = json.dumps(message)
        for connection in list(self.active_connections):  # Kopiere Liste um Concurrency-Probleme zu vermeiden
            try:
                await connection.send_text(data)
            except Exception as e:
                logging.error(f"Fehler beim Senden von Daten an {connection.client}: {e}")
                self.disconnect(connection)

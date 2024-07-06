# WebSocket connection manager class
from typing import List
from fastapi import WebSocket
from config.log_config import logger

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        logger.info("ConnectionManager initialized")

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connection established: {websocket.client.host}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket connection disconnected: {websocket.client.host}")

    async def broadcast(self, data: dict):
        logger.info(f"Broadcasting message to {len(self.active_connections)} connections: {data}")
        for connection in self.active_connections:
            await connection.send_json(data)

manager = ConnectionManager()

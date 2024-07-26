
from fastapi import WebSocket, WebSocketDisconnect
from Manager.WebSocket import manager
from config.log_config import logger


# Common WebSocket endpoint handler
async def common_websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
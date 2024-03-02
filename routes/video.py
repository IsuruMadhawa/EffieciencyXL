from fastapi import APIRouter, WebSocket
import asyncio
import websockets

router = APIRouter(
    prefix="/api/video",
    tags=["video"],
    responses={404: {"description": "The requested uri was not found"}},
)


@router.websocket("/video")
async def video_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        with open('video.mp4', 'ab') as f:
            f.write(data)

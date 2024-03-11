import cv2
import numpy as np
from fastapi import APIRouter, WebSocket

from ML.face_rec import recognize_face, compute_face_descriptors

router = APIRouter(
    prefix="/api/video",
    tags=["video"],
    responses={404: {"description": "The requested uri was not found"}},
)

# Load the face descriptors and labels once when the server starts
face_descriptors, face_labels = compute_face_descriptors("dataset")


@router.websocket("/video")
async def video_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()

        # Convert the bytes to a numpy array
        nparr = np.frombuffer(data, np.uint8)

        # Decode the numpy array as an image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Run the face recognition on the image
        label = recognize_face(face_descriptors, face_labels, img)

        # Send the result back to the client
        await websocket.send_text(f"The face is recognized as: {label}")
        # TODO add to the database

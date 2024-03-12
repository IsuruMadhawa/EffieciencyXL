import cv2
import numpy as np
from fastapi import APIRouter, WebSocket
from concurrent.futures import ThreadPoolExecutor

from facerec.main import compute_face_descriptors, recognize_face
from services.videostream_service import add_video_data

router = APIRouter(
    prefix="/api/video",
    tags=["video"],
    responses={404: {"description": "The requested uri was not found"}},
)

# Load the face descriptors and labels once when the server starts
face_descriptors, face_labels = compute_face_descriptors("facerec/dataset")

executor = ThreadPoolExecutor(max_workers=1)


@router.websocket("/video")
async def video_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()

        location = "current_location"
        misc = "no misc data available"

        # Convert the bytes to a numpy array
        nparr = np.frombuffer(data, np.uint8)

        # Decode the numpy array as an image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Run the face recognition on the image
        label = recognize_face(face_descriptors, face_labels, img)

        # Convert the image to binary format
        is_success, im_buf_arr = cv2.imencode(".jpg", img)
        byte_im = im_buf_arr.tobytes()

        # add to the database
        executor.submit(add_video_data, label, location, misc, byte_im)
        # TODO store the image in the database

        # Send the result back to the client
        await websocket.send_text(f"The face is recognized as: {label}")

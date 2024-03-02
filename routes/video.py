from fastapi import APIRouter

router = APIRouter(
    prefix="/api/video",
    tags=["video"],
    responses={404: {"description": "The requested page was not found"}},
)

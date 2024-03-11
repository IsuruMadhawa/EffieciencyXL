

router = APIRouter(
    prefix="/api/video",
    tags=["video"],
    responses={404: {"description": "The requested uri was not found"}},
)

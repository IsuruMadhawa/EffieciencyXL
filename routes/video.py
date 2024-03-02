router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "The requested page was not found"}},
)
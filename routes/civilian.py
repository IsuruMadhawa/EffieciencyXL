from fastapi import APIRouter

router = APIRouter(
    prefix="/api/civilian",
    tags=["civilian"],
    responses={404: {"description": "The requested uri was not found"}},
)


@router.post("/request-clearance")
async def 

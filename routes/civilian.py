from fastapi import APIRouter

router = APIRouter(
    prefix="/api/civilian",
    tags=["civilian"],
    responses={404: {"description": "The requested uri was not found"}},
)


@router.post("/request-clearance")
async def request_clearance(
        name: str = Form(...),
        division: str = Form(...),
        district: str = Form(...),
        token: str = Depends(oauth2_scheme)
):
    return {"message": "Request for clearance is sent"}

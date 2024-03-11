from fastapi import APIRouter

from auth.authorize import get_current_user, credentials_exception

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
    """
    The endpoint for requesting clearance reports
    Args:
        name: name of the civilian
        division: police division
        district: district
        token: access token

    Returns:

    """
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "civilian":
        return {"message": "Only civilians can request clearance"}

    # TODO Add the request to the database

    return {"message": "Request for clearance is sent"}

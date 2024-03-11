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
    """
    The endpoint for requesting clearance reports
    Args:
        name: name of the civilian
        division: police division
        district: district
        token: access token

    Returns:

    """
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is blacklisted"
        )
    user = get_current_user(token)
    return {"message": "Request for clearance is sent"}

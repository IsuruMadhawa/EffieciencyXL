from fastapi import APIRouter, Depends, Form

from auth.authorize import get_current_user, credentials_exception, oauth2_scheme

router = APIRouter(
    prefix="/api/civilian",
    tags=["civilian"],
    responses={404: {"description": "The requested uri was not found"}},
)


@router.post("/get-lost-item-reports")
async def lost_item_report(
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can report lost item reports"}

    pass  # TODO


@router.post("/get-clearance-requests")
async def request_clearance(
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can request clearance reports"}

    pass  # TODO


@router.post("/approve-clearance-report")
async def approve_clearance_report(
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can approve clearance reports"}

    pass  # TODO

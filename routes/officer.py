from fastapi import APIRouter, Depends, Form

from auth.authorize import get_current_user, credentials_exception, oauth2_scheme
from mailer import send_mail
from services.officer_service import get_all_clearance_requests, get_all_lost_item_reports, \
    get_single_clearance_request, update_clearance_report

router = APIRouter(
    prefix="/api/officer",
    tags=["officer"],
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

    return get_all_lost_item_reports()


@router.post("/get-clearance-requests")
async def request_clearance(
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can request clearance reports"}

    return get_all_clearance_requests()


@router.post("/approve-clearance-report")
async def approve_clearance_report(
        r_id: int = Form(...),
        details: str = Form(...),
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can approve clearance reports"}

    report = get_single_clearance_request(r_id)
    o_id = get_officer_id(user.id)

    update_clearance_report(r_id, o_id, details)

    # notify the civilian
    user_email = report.c_email
    send_mail(
        user_email,
        "Your clearance report has been approved"
    )

    # TODO implement this
    pass

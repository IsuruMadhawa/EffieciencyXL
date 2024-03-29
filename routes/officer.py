from fastapi import APIRouter, Depends, Form

from auth.authorize import get_current_user, credentials_exception, oauth2_scheme
from mailer import send_mail
from services.officer_service import get_all_clearance_requests, get_all_lost_item_reports, \
    get_single_clearance_request, update_clearance_report, get_officer_id, all_complaints, get_all_criminals, \
    add_new_criminal, get_criminal_sightings, get_alerts

router = APIRouter(
    prefix="/api/officer",
    tags=["officer"],
    responses={404: {"description": "The requested uri was not found"}},
)


@router.post("/get-alerts")
async def alerts(
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    officer = get_officer_id(user.id)

    if officer is None:
        return {"message": "Only officers can request criminal sighting alerts"}

    return get_alerts()


@router.post("/criminal-sightings")
async def criminal_sightings(
        name: str = Form(...),
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    officer = get_officer_id(user.id)

    if officer is None:
        return {"message": "Only officers can report criminal sightings"}

    return get_criminal_sightings(name)


@router.post("/criminals")
async def all_criminals(
    token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can get all complaints"}

    return get_all_criminals()


@router.post("/add-criminal")
async def add_criminal(
    name: str = Form(...),
    age: int = Form(...),
    division: str = Form(...),
    district: str = Form(...),
    description: str = Form(...),
    token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can add criminals"}

    return add_new_criminal(name, age, description, division, district)


@router.post("/get-all-complaints")
async def get_all_complaints(
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can get all complaints"}

    return all_complaints()


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
async def request_clearance_reports(
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can request clearance reports"}

    return get_all_clearance_requests()


@router.post("/disapprove-clearance-report")
async def disapprove_clearance_report(
        r_id: int = Form(...),
        details: str = Form(...),
        token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(token)

    if user is None:
        raise credentials_exception

    if user.role != "officer":
        return {"message": "Only officers can disapprove clearance reports"}

    report = get_single_clearance_request(r_id)
    print(report[0][7])
    o_id = get_officer_id(user.id)[0]

    result = update_clearance_report(r_id, o_id, details, "disapproved")

    # TODO Uncomment this
    # notify the civilian
    # user_email = report[0][7]
    # send_mail(
    #     user_email,
    #     "Your clearance report has been disapproved"
    # )

    return result


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
    print(report[0][7])
    o_id = get_officer_id(user.id)[0]

    result = update_clearance_report(r_id, o_id, details, "approved")

    # TODO Uncomment this
    # notify the civilian
    # user_email = report[0][7]
    # send_mail(
    #     user_email,
    #     "Your clearance report has been approved"
    # )

    return result

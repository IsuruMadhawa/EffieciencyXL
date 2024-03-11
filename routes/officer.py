from fastapi import APIRouter, Depends, Form

from auth.authorize import get_current_user, credentials_exception, oauth2_scheme
from services.civilian_service import clearance_request, add_lost_item_report

router = APIRouter(
    prefix="/api/civilian",
    tags=["civilian"],
    responses={404: {"description": "The requested uri was not found"}},
)


@router.post("/lost-item-report")
async def lost_item_report(
        name: str = Form(...),
        division: str = Form(...),
        district: str = Form(...),
        item: str = Form(...),
        description: str = Form(...),
        token: str = Depends(oauth2_scheme)
):


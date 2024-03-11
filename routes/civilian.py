from fastapi import APIRouter

router = APIRouter(
    prefix="/api/civilian",
    tags=["civilian"],
    responses={404: {"description": "The requested uri was not found"}},
)


@router.post("/request-clearance")
async def request_clearance(
        
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return {"message": "Request for clearance is sent"}

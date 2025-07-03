import fastapi
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.application import ApplicationRequest
from core.services.interfaces.application import IApplicationService
from core.services.providers.application import get_application_service

router = fastapi.APIRouter(prefix="/application", tags=["application"])

@router.get("/")
async def get____(
        user: User = Depends(get_user),
) -> JSONResponse:
    ...

@router.post("/")
async def send_application_to_vacancy(
        respond_to_vacancy: ApplicationRequest = Body(...),
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:

    try:
        await application_service.create_application(
            user_id=user.id,
            vacancy_id=respond_to_vacancy.vacancy_id,
            description=respond_to_vacancy.description,
        )
        return JSONResponse({'body': 'ok'})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




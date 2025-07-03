import fastapi
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.application import ApplicationRequest, ApplicationShortInfo, ApplicationMainInfo, \
    UserApplicationsInOrganizationRequest, ApplicationCancelByUserRequest, ApplicationActivityStatusType
from core.services.interfaces.application import IApplicationService
from core.services.interfaces.permission import IPermissionService
from core.services.providers.application import get_application_service
from core.services.providers.permission import get_permission_service
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.exceptions.permission import PermissionDenied

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


@router.post("/my", response_model=ApplicationMainInfo)
async def user_respond_applications(
        request_model: UserApplicationsInOrganizationRequest = Body(...),
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:
    """
    Отклики совершенные пользователем (по умолчанию все. Потом добавить фильтрацию)
    """
    try:
        res = await application_service.get_user_applications_main_info_in_organization(
            user_id=user.id,
            org_id=request_model.org_id,
        )
        res = [i.model_dump() for i in res]

        return JSONResponse({'body': res})

    except EntityDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/my/cancel")
async def cancel_user_application_by_yourself(
        request_model: ApplicationCancelByUserRequest = Body(...),
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
        permission_service: IPermissionService = Depends(get_permission_service)
) -> JSONResponse:
    """
    Отклонить отклик (свой. --- т.е. От лица пользователя)
    """

    # Пользователь должен являться владельцем отклика
    flag = await permission_service.can_user_edit_yourself_application(
        user_id=user.id,
        application_id=request_model.application_id,
    )
    if not flag:
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        res = await application_service.cancel_application(
            application_id=request_model.application_id,
        )
        res = res.model_dump()
        return JSONResponse({'body': res})

    except EntityDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/manage")
async def manager_applications(
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:
    """
    Отклики на вакансии которыми пользователь может управлять как менеджер
    (например отправлять офферы)
    """
    try:
        return JSONResponse({'body': 'заглушка'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/manage/reject")
async def manager_applications(
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:
    """
    Отклонить отклик / реджектнуть (чужой. --- т.е. От лица менеджера)
    """
    try:
        return JSONResponse({'body': 'заглушка'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

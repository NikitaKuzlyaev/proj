from typing import Sequence

import fastapi
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.application import ApplicationRequest, ApplicationShortInfo, ApplicationMainInfo, \
    UserApplicationsInOrganizationRequest, ApplicationCancelByUserRequest, ApplicationActivityStatusType, ApplicationId, \
    ApplicationLimits
from core.services.interfaces.application import IApplicationService
from core.services.interfaces.permission import IPermissionService
from core.services.providers.application import get_application_service
from core.services.providers.permission import get_permission_service
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.exceptions.domain import ActiveEntityLimit
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from core.utilities.exceptions.permission import PermissionDenied

router = fastapi.APIRouter(prefix="/application", tags=["application"])


@router.get("/")
async def get____(
        user: User = Depends(get_user),
) -> JSONResponse:
    ...


@router.post(
    path="/",
    response_model=ApplicationId,
    status_code=201,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
        ActiveEntityLimit: (409, None),
    }
)
async def send_application_to_vacancy(
        params: ApplicationRequest = Body(...),
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:
    """
    Пользователь делает отклик на вакансию
    """
    result: ApplicationId = (
        await application_service.create_application(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.post(
    path="/my/limits",
    response_model=ApplicationLimits,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def limits_of_user_active_applications_in_organization(
        params: UserApplicationsInOrganizationRequest = Body(...),
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:
    """
    Узнать текущее и максимальное число активных откликов пользователя в организации
    """
    result: ApplicationLimits = (
        await application_service.get_user_application_limits_in_organization(
            user_id=user.id,
            org_id=params.org_id,
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.post(
    path="/my",
    response_model=ApplicationMainInfo,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def user_respond_applications(
        params: UserApplicationsInOrganizationRequest = Body(...),
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:
    """
    Отклики совершенные пользователем (по умолчанию все. Потом добавить фильтрацию)
    """
    result: Sequence[ApplicationMainInfo] = (
        await application_service.get_user_applications_main_info_in_organization(
            user_id=user.id,
            org_id=params.org_id,
        )
    )
    result = [i.model_dump() for i in result]

    return JSONResponse({'body': result})


@router.post(
    path="/my/cancel",
)
@async_http_exception_mapper(
    mapping={
        EntityDoesNotExist: (404, None),
    }
)
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

    res = await application_service.cancel_application(
        application_id=request_model.application_id,
    )
    res = res.model_dump()
    return JSONResponse({'body': res})


@router.get(
    path="/manage",
)
@async_http_exception_mapper(

)
async def manager_applications(
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:
    """
    Отклики на вакансии которыми пользователь может управлять как менеджер
    (например отправлять офферы)
    """
    return JSONResponse({'body': 'заглушка'})


@router.post(
    path="/manage/reject",
)
@async_http_exception_mapper(

)
async def manager_application_reject(
        user: User = Depends(get_user),
        application_service: IApplicationService = Depends(get_application_service),
) -> JSONResponse:
    """
    Отклонить отклик / реджектнуть (чужой. --- т.е. От лица менеджера)
    """
    return JSONResponse({'body': 'заглушка'})

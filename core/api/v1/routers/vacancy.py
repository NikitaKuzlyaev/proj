import fastapi
from fastapi import Depends, Body
from fastapi import Query
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.permission import PermissionsShortResponse
from core.schemas.vacancy import VacancyCreateRequest, VacancyPatchRequest, VacancyShortInfoResponse, \
    VacancyCreateResponse, VacancyPatchResponse
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.vacancy import IVacancyService
from core.services.providers.permission import get_permission_service
from core.services.providers.vacancy import get_vacancy_service
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper

router = fastapi.APIRouter(prefix="/vacancy", tags=["vacancy"])


@router.get(
    path="/short-info",
    response_model=VacancyShortInfoResponse,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        EntityDoesNotExist: (404, None),
    }
)
async def get_vacancy_short_info(
        vacancy_id: int = Query(),
        user: User = Depends(get_user),
        vacancy_service: IVacancyService = Depends(get_vacancy_service),
) -> JSONResponse:
    #
    # Настроить проверку прав
    #

    res: VacancyShortInfoResponse = (
        await vacancy_service.get_vacancy_short_info_response(
            vacancy_id=vacancy_id,
            user_id=user.id)
    )
    res = res.model_dump()
    return JSONResponse({"body": res})


@router.post(
    path="/",
    response_model=VacancyCreateResponse,
    status_code=201,
)
@async_http_exception_mapper(
    mapping={
        EntityDoesNotExist: (404, None),
    }
)
async def create_vacancy(
        vacancy_create_schema: VacancyCreateRequest = Body(...),
        user: User = Depends(get_user),
        vacancy_service: IVacancyService = Depends(get_vacancy_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    result: VacancyCreateResponse = (
        await vacancy_service.create_vacancy(
            user_id=user.id,
            **vacancy_create_schema.model_dump(),
        )
    )
    permission: PermissionsShortResponse = (
        await permission_service.allow_user_edit_vacancy(
            user_id=user.id,
            vacancy_id=result.vacancy_id,
        )
    )
    result = result.model_dump()
    return JSONResponse({"body": result})


@router.patch(
    path="/",
    response_model=VacancyPatchResponse,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        EntityDoesNotExist: (404, None),
    }
)
async def patch_vacancy(
        vacancy_patch_schema: VacancyPatchRequest = Body(...),
        user: User = Depends(get_user),
        vacancy_service: IVacancyService = Depends(get_vacancy_service),
) -> JSONResponse:
    vacancy_patch_response: VacancyPatchResponse = (
        await vacancy_service.patch_vacancy(
            user_id=user.id,
            **vacancy_patch_schema.model_dump(),
        )
    )
    vacancy_patch_response = vacancy_patch_response.model_dump()
    return JSONResponse({"body": vacancy_patch_response})

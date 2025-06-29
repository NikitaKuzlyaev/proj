import fastapi
from fastapi import Depends, Body
from fastapi import Query
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.vacancy import VacancyCreateRequest, VacancyPatchRequest, VacancyShortInfoResponse, \
    VacancyCreateResponse, VacancyPatchResponse
from core.services.domain.vacancy import VacancyService, get_vacancy_service

router = fastapi.APIRouter(prefix="/vacancy", tags=["vacancy"])


@router.get("/short-info")
async def get_vacancy_short_info(
        vacancy_id: int = Query(),
        user: User = Depends(get_user),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
) -> JSONResponse:
    try:
        res: VacancyShortInfoResponse = (
            await vacancy_service.get_vacancy_short_info_response(
                vacancy_id=vacancy_id,
                user_id=user.id)
        )
        res = res.model_dump()
        return JSONResponse({"body": res})
    except Exception as e:
        return JSONResponse({"body": str(e)})


@router.post("/", response_model=VacancyCreateResponse)
async def create_vacancy(
        vacancy_create_schema: VacancyCreateRequest = Body(...),
        user: User = Depends(get_user),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
) -> JSONResponse:
    try:
        vacancy_create_response: VacancyCreateResponse = (
            await vacancy_service.create_vacancy(
                user_id=user.id,
                **vacancy_create_schema.model_dump(),
            )
        )
        vacancy_create_response = vacancy_create_response.model_dump()
        return JSONResponse({"body": vacancy_create_response})
    except Exception as e:
        return JSONResponse({"body": str(e)})


@router.patch("/", response_model=VacancyPatchResponse)
async def patch_vacancy(
        vacancy_patch_schema: VacancyPatchRequest = Body(...),
        user: User = Depends(get_user),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
) -> JSONResponse:
    try:
        vacancy_patch_response: VacancyPatchResponse = (
            await vacancy_service.patch_vacancy(
                user_id=user.id,
                **vacancy_patch_schema.model_dump(),
            )
        )
        vacancy_patch_response = vacancy_patch_response.model_dump()
        return JSONResponse({"body": vacancy_patch_response})
    except Exception as e:
        return JSONResponse({"body": str(e)})

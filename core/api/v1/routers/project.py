from typing import Sequence

import fastapi
from fastapi import Depends, Body
from fastapi import Query, HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.project import ProjectCreateRequest, ProjectFullInfoResponse, ProjectPatchRequest, \
    ProjectVacanciesShortInfoResponse, CreatedProjectResponse, PatchedProjectResponse
from core.services.domain.project import get_project_service, ProjectService
from core.services.domain.vacancy import VacancyService, get_vacancy_service

router = fastapi.APIRouter(prefix="/project", tags=["project"])


@router.get("/full-info", response_model=ProjectFullInfoResponse)
async def get_project_full_info(
        project_id: int = Query(),
        user: User = Depends(get_user),
        project_service: ProjectService = Depends(get_project_service),
) -> JSONResponse:
    try:
        res: ProjectFullInfoResponse = (
            await project_service.get_project_full_info_response(
                project_id=project_id,
                user_id=user.id,
            )
        )
        res = res.model_dump()
        return JSONResponse({'body': res})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vacancies-info", response_model=Sequence[ProjectVacanciesShortInfoResponse])
async def get_vacancies_info_in_project(
        project_id: int = Query(),
        user: User = Depends(get_user),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
) -> JSONResponse:
    try:
        vacancies_with_short_info: Sequence[ProjectVacanciesShortInfoResponse] = (
            await vacancy_service.get_all_vacancies_in_project_detailed_info(
                project_id=project_id,
                user_id=user.id,
            )
        )
        res = [row.model_dump() for row in vacancies_with_short_info]
        return JSONResponse({'body': res})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=CreatedProjectResponse)
async def create_project(
        user: User = Depends(get_user),
        project_create_schema: ProjectCreateRequest = Body(...),
        project_service: ProjectService = Depends(get_project_service),
) -> JSONResponse:
    try:
        created_project_schema: CreatedProjectResponse = (
            await project_service.create_project(
                user_id=user.id,
                **project_create_schema.model_dump(),
            )
        )
        created_project_schema = created_project_schema.model_dump()
        return JSONResponse({"body": created_project_schema})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/", response_model=PatchedProjectResponse)
async def patch_project(
        user: User = Depends(get_user),
        project_patch_schema: ProjectPatchRequest = Body(...),
        project_service: ProjectService = Depends(get_project_service),
) -> JSONResponse:
    try:
        patched_project_schema: PatchedProjectResponse = (
            await project_service.patch_project(
                user_id=user.id,
                **project_patch_schema.model_dump(),
            )
        )
        patched_project_schema = patched_project_schema.model_dump()
        return JSONResponse({"body": patched_project_schema})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/", response_class=HTMLResponse)
async def delete_project():
    ...

from typing import Sequence

import fastapi
from fastapi import Depends, Body
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.application import ApplicationShortInfo
from core.schemas.project import ProjectCreateRequest, ProjectFullInfoResponse, ProjectPatchRequest, \
    ProjectVacanciesFullInfoResponse, CreatedProjectResponse, PatchedProjectResponse
from core.services.interfaces.application import IApplicationService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.project import IProjectService
from core.services.interfaces.vacancy import IVacancyService
from core.services.mappers.vacancy import VacancyMapper, get_vacancy_mapper
from core.services.providers.application import get_application_service
from core.services.providers.permission import get_permission_service
from core.services.providers.project import get_project_service
from core.services.providers.vacancy import get_vacancy_service
from core.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/project", tags=["project"])


@router.get("/full-info",
            response_model=ProjectFullInfoResponse,
            status_code=200)
async def get_project_full_info(
        project_id: int = Query(...,),
        user: User = Depends(get_user),
        project_service: IProjectService = Depends(get_project_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:

    # Пользователь должен иметь права на просмотр проекта
    flag = await permission_service.can_user_see_project(user_id=user.id, project_id=project_id)
    if not flag: raise HTTPException(status_code=403, detail="Not allowed")

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


@router.get("/vacancies-info", response_model=Sequence[ProjectVacanciesFullInfoResponse])
async def get_vacancies_info_in_project(
        project_id: int = Query(),
        user: User = Depends(get_user),
        vacancy_service: IVacancyService = Depends(get_vacancy_service),
        vacancy_mapper: VacancyMapper = Depends(get_vacancy_mapper),
        application_service: IApplicationService = Depends(get_application_service)
) -> JSONResponse:
    try:
        vacancies_with_short_info: Sequence[ProjectVacanciesFullInfoResponse] = (
            await vacancy_service.get_all_vacancies_in_project_detailed_info(
                project_id=project_id,
                user_id=user.id,
            )
        )
        user_active_applications_in_this_project: Sequence[ApplicationShortInfo] = (
            await application_service.get_all_active_applications_by_user_and_project(
                user_id=user.id,
                project_id=project_id,
            )
        )
        res = vacancy_mapper.update_vacancies_full_info_response_by_active_applications(
            base=vacancies_with_short_info,
            active_applications=user_active_applications_in_this_project,
        )

        res = [row.model_dump() for row in res]

        return JSONResponse({'body': res})

    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=CreatedProjectResponse)
async def create_project(
        user: User = Depends(get_user),
        project_create_schema: ProjectCreateRequest = Body(...),
        project_service: IProjectService = Depends(get_project_service),
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
        project_service: IProjectService = Depends(get_project_service),
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
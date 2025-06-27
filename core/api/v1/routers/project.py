from typing import Sequence

import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.dependencies.repository import get_repository
from core.models import Organization, Project, User, Vacancy
from core.repository.crud.organization import OrganizationCRUDRepository
#from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.user import UserCRUDRepository
from core.schemas.project import ProjectInCreate, ProjectCreateRequest, ProjectFullInfoRequest, ProjectManagerInfo, \
    ProjectVisibilityType, ProjectActivityStatusType, ProjectPatchRequest, ProjectVacanciesShortInfoResponse, \
    ProjectOfVacancyInfo
from core.schemas.vacancy import VacancyActivityStatusType, VacancyVisibilityType
from core.services.domain.organization import OrganizationService, get_organization_service
from core.services.domain.project import get_project_service, ProjectService
from core.services.domain.vacancy import VacancyService, get_vacancy_service
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/project", tags=["project"])

from templates import templates

"""
    ----------------------------------------------------------
"""


@router.get("/", response_class=HTMLResponse)
async def get_projects_in_folder(request: Request, response: Response):
    ...


@router.get("/main-info", response_class=HTMLResponse)
async def get_project_main_info(request: Request, response: Response):
    ...


@router.get("/full-info", response_model=ProjectFullInfoRequest)
async def get_projects_full_info(
        request: Request,
        response: Response,
        project_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
) -> JSONResponse:
    try:

        project: Project = \
            await project_service.get_project_by_id(
                project_id=project_id
            )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        manager: User = project.creator

        res = ProjectFullInfoRequest(
            org_id=project.organization_id,
            name=project.name,
            short_description=project.short_description,
            long_description=project.long_description,
            manager=ProjectManagerInfo(
                user_id=manager.id,
                name=manager.username,
                avatar=''
            ),
            visibility=ProjectVisibilityType(project.visibility),
            activity_status=ProjectActivityStatusType(project.activity_status),
            team_current_size=0,
            team_full_size=0,
            open_vacancies=0
        ).model_dump()

        print(res)
        return JSONResponse({'body': res})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/vacancies-info", response_model=Sequence[ProjectVacanciesShortInfoResponse])
async def get_vacancies_info_in_project(
        request: Request,
        response: Response,
        project_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
) -> JSONResponse:

    try:

        project: Project = \
            await project_service.get_project_by_id(
                project_id=project_id
            )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        vacancies_with_short_info: Sequence[ProjectVacanciesShortInfoResponse] = \
            await vacancy_service.get_all_vacancies_in_project_detailed_info(
                project_id=project.id,
                user_id=user.id,
            )

        res = [row.model_dump() for row in vacancies_with_short_info]

        return JSONResponse({'body': res})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_class=JSONResponse)
async def create_project(
        request: Request,
        response: Response,
        project_create_schema: ProjectCreateRequest = Body(...),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
) -> JSONResponse:
    org: Organization = \
        await organization_service.get_organization_by_id(
            org_id=project_create_schema.org_id
        )
    if not org:
        raise HTTPException(status_code=404)

    project: Project = \
        await project_service.create_project(
            user_id=user.id,
            project_create_schema=project_create_schema
        )

    return JSONResponse({"body": 'ok'})


@router.patch("/", response_class=HTMLResponse)
async def patch_project(
        request: Request,
        response: Response,
        project_patch_schema: ProjectPatchRequest = Body(...),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
) -> JSONResponse:
    org: Organization = \
        await organization_service.get_organization_by_id(
            org_id=project_patch_schema.org_id
        )
    if not org:
        raise HTTPException(status_code=404)

    # сделать проверку прав!!!

    project: Project = \
        await project_service.patch_project(
            project_patch_schema=project_patch_schema
        )

    return JSONResponse({"body": 'ok'})


@router.delete("/", response_class=HTMLResponse)
async def delete_project(request: Request, response: Response):
    ...


"""
    ----------------------------------------------------------
"""

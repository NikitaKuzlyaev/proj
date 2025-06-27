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
from core.schemas.vacancy import VacancyActivityStatusType, VacancyVisibilityType, VacancyCreateRequest, \
    VacancyPatchRequest, VacancyShortInfoResponse
from core.services.domain.organization import OrganizationService, get_organization_service
from core.services.domain.project import get_project_service, ProjectService
from core.services.domain.vacancy import VacancyService, get_vacancy_service
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/vacancy", tags=["vacancy"])

from templates import templates

"""
    ----------------------------------------------------------
"""


@router.get("/short-info")
async def get_vacancy_short_info(
        request: Request,
        response: Response,
        vacancy_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
) -> JSONResponse:

    vacancy: Vacancy = \
        await vacancy_service.get_vacancy_by_id(
            vacancy_id=vacancy_id,
        )

    res = VacancyShortInfoResponse(
        vacancy_id=vacancy.id,
        project_id=vacancy.project_id,
        name=vacancy.name,
        short_description=vacancy.short_description,
        activity_status=VacancyActivityStatusType(vacancy.activity_status),
        visibility=VacancyVisibilityType(vacancy.visibility),
    ).model_dump()

    return JSONResponse({"body": res})

@router.post("/", response_class=JSONResponse)
async def create_vacancy(
        request: Request,
        response: Response,
        vacancy_create_schema: VacancyCreateRequest = Body(...),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
) -> JSONResponse:

    project: Project = \
        await project_service.get_project_by_id(
            project_id=vacancy_create_schema.project_id
        )
    if not project:
        raise HTTPException(status_code=404)

    vacancy: Vacancy = \
        await vacancy_service.create_vacancy(
            user_id=user.id,
            vacancy_create_schema=vacancy_create_schema,
        )

    return JSONResponse({"body": 'ok'})


@router.patch("/")
async def patch_vacancy(
        request: Request,
        response: Response,
        vacancy_patch_schema: VacancyPatchRequest = Body(...),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
) -> JSONResponse:
    project: Project = \
        await project_service.get_project_by_id(
            project_id=vacancy_patch_schema.project_id
        )
    if not project:
        raise HTTPException(status_code=404)

    # сделать проверку прав!!!

    vacancy: Vacancy = \
        await vacancy_service.patch_vacancy(
            vacancy_patch_schema=vacancy_patch_schema
        )

    return JSONResponse({"body": 'ok'})



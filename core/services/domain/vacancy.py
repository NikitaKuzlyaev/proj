import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from typing import Sequence

from core.dependencies.repository import get_repository
from core.models import Organization, Project
from core.models.organizationMember import OrganizationMember
# from core.repository.crud.folder import FolderCRUDRepository
# from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.schemas.project import ProjectCreateRequest, ProjectPatchRequest, ProjectVacanciesShortInfoResponse
from core.schemas.vacancy import VacancyCreateRequest, VacancyPatchRequest
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)
from core.models.user import User
from core.schemas.organization import OrganizationInCreate, OrganizationCreateInRequest
# from core.schemas.folder import RootFolderInCreate
# from core.models.folder import Folder
from core.dependencies.authorization import get_user
from core.models.vacancy import Vacancy


class VacancyService:
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            project_repo: ProjectCRUDRepository,
            vacancy_repo: VacancyCRUDRepository,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.project_repo = project_repo
        self.vacancy_repo = vacancy_repo

    async def get_all_vacancies_in_project(
            self,
            project_id: int,
    ) -> Sequence[Vacancy]:
        res: Sequence[Vacancy] = \
            await self.vacancy_repo.get_all_vacancies_in_project(
                project_id=project_id
            )
        return res

    async def get_all_vacancies_in_project_detailed_info(
            self,
            project_id: int,
            user_id: int
    ) -> Sequence[ProjectVacanciesShortInfoResponse]:
        res: Sequence[ProjectVacanciesShortInfoResponse] = \
            await self.vacancy_repo.get_all_vacancies_in_project_detailed_info(
                project_id=project_id,
                user_id=user_id
            )
        return res

    async def get_vacancy_by_id(
            self,
            vacancy_id: int,
    ) -> Vacancy:
        res: Vacancy = \
            await self.vacancy_repo.get_vacancy_by_id(
                vacancy_id=vacancy_id
            )
        return res

    async def create_vacancy(
            self,
            user_id: int,
            vacancy_create_schema: VacancyCreateRequest
    ) -> Vacancy:
        new_vacancy: Vacancy = \
            await self.vacancy_repo.create_vacancy(
                project_id=vacancy_create_schema.project_id,
                user_id=user_id,
                name=vacancy_create_schema.name,
                short_description=vacancy_create_schema.short_description,
                activity_status=vacancy_create_schema.activity_status.value,
                visibility=vacancy_create_schema.visibility.value,
            )
        return new_vacancy

    async def patch_vacancy(
            self,
            vacancy_patch_schema: VacancyPatchRequest
    ) -> Vacancy:
        try:
            vacancy: Vacancy = \
                await self.vacancy_repo.patch_vacancy_by_id(
                    vacancy_id=vacancy_patch_schema.vacancy_id,
                    project_id=vacancy_patch_schema.project_id,
                    name=vacancy_patch_schema.name,
                    short_description=vacancy_patch_schema.short_description,
                    visibility=vacancy_patch_schema.visibility.value,
                    activity_status=vacancy_patch_schema.activity_status.value,
                )
            return vacancy
        except Exception as e:
            raise e


def get_vacancy_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
        vacancy_repo: VacancyCRUDRepository = Depends(get_repository(VacancyCRUDRepository)),
) -> VacancyService:
    return VacancyService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        project_repo=project_repo,
        vacancy_repo=vacancy_repo,
    )

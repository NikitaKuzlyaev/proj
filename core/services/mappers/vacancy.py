import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from typing import Sequence

from starlette.responses import JSONResponse

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
from core.schemas.vacancy import VacancyCreateRequest, VacancyPatchRequest, VacancyShortInfoResponse, \
    VacancyActivityStatusType, VacancyVisibilityType, VacancyCreateResponse, VacancyPatchResponse
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


class VacancyMapper:
    def __init__(
            self,
    ):
        return

    def vacancy_to_short_info_response(
            self,
            vacancy: Vacancy,
    ) -> VacancyShortInfoResponse:
        res = VacancyShortInfoResponse(
            vacancy_id=vacancy.id,
            project_id=vacancy.project_id,
            name=vacancy.name,
            short_description=vacancy.short_description,
            activity_status=VacancyActivityStatusType(vacancy.activity_status),
            visibility=VacancyVisibilityType(vacancy.visibility),
        )
        return res

    def vacancy_to_create_response(
            self,
            vacancy: Vacancy
    ) -> VacancyCreateResponse:
        res = VacancyCreateResponse(
            vacancy_id=vacancy.id,
        )
        return res

    def vacancy_to_patch_response(
            self,
            vacancy: Vacancy
    ) -> VacancyPatchResponse:
        res = VacancyPatchResponse(
            vacancy_id=vacancy.id,
        )
        return res


def get_vacancy_mapper(

) -> VacancyMapper:
    return VacancyMapper(

    )

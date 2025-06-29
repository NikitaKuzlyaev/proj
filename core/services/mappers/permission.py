import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from typing import Sequence

from core.dependencies.repository import get_repository
from core.models import Organization, Project, Permission
from core.models.organizationMember import OrganizationMember
# from core.repository.crud.folder import FolderCRUDRepository
# from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.schemas.permission import PermissionsShortResponse
from core.schemas.project import ProjectCreateRequest, ProjectPatchRequest, ProjectVacanciesShortInfoResponse, \
    ProjectFullInfoResponse, ProjectManagerInfo, ProjectVisibilityType, ProjectActivityStatusType, \
    CreatedProjectResponse, PatchedProjectResponse
from core.schemas.vacancy import VacancyCreateRequest, VacancyPatchRequest, VacancyShortInfoResponse, \
    VacancyActivityStatusType, VacancyVisibilityType
from core.services.mappers.vacancy import VacancyMapper, get_vacancy_mapper
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


class PermissionMapper:
    def __init__(
            self,
    ):
        return

    def get_short_permission_response(
            self,
            permission: Permission,
    ) -> PermissionsShortResponse:
        res = PermissionsShortResponse(
            permission_id=permission.id,
        )
        return res


def get_permission_mapper(

) -> PermissionMapper:
    return PermissionMapper(

    )

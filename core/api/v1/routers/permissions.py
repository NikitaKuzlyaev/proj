from typing import List

import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from typing import Sequence
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user, oauth2_scheme
from core.dependencies.repository import get_repository
from core.models import User, Organization, Project

from core.repository.crud.user import UserCRUDRepository
from core.services.domain.organization import OrganizationService, get_organization_service
from core.services.domain.permission import PermissionService, get_permission_service
from core.services.domain.project import get_project_service, ProjectService
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/permissions", tags=["permissions"])

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.user import UserCreate, UserOut, Token
from core.services.domain import auth as auth_service
from fastapi import Security
from core.schemas.permission import PermissionsResponse

ALL_FIELDS = PermissionsResponse.model_fields.keys()

@router.get("/", response_model=PermissionsResponse)
async def permissions(
        user: User = Depends(get_user),
        fields: List[str] = Query(default=[]),
):
    # Если ничего не передали — вернуть всё
    selected_fields = set(fields) if fields else set(ALL_FIELDS)

    result = {}
    print(fields)

    if "can_create_global_organizations" in selected_fields:
        result["can_create_global_organizations"] = True

    return result


@router.get("/is-user-allowed-to-create-projects-inside-organization", response_model=bool)
async def can_user_create_projects_inside_organization(
        request: Request,
        response: Response,
        org_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
        permission_service: PermissionService = Depends(get_permission_service),
) -> JSONResponse:
    try:

        org: Organization = \
            await organization_service.get_organization_by_id(
                org_id=org_id
            )
        if not org:
            return JSONResponse({'body': False})

        flag: bool = \
            await permission_service.can_user_create_projects_inside_organization(
                org_id=org_id,
                user_id=user.id
            )

        return JSONResponse({'body': flag})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/is-user-allowed-to-edit-project", response_model=bool)
async def can_user_edit_project(
        request: Request,
        response: Response,
        project_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        project_service: ProjectService = Depends(get_project_service),
        permission_service: PermissionService = Depends(get_permission_service),
) -> JSONResponse:
    try:

        project: Project = \
            await project_service.get_project_by_id(
                project_id=project_id
            )
        if not project:
            return JSONResponse({'body': False})

        flag: bool = \
            await permission_service.can_user_edit_project(
                project_id=project_id,
                user_id=user.id
            )

        return JSONResponse({'body': flag})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.get("/p", response_model=PermissionsResponse)
# async def check_permission(
#         user: User = Depends(get_user),
#         resourse_type: str = Query(),
#         resourse_id: ind = Query(),
#
#
# ) -> JSONResponse:
#
#     flag = False
#
#     return JSONResponse({"body": flag})


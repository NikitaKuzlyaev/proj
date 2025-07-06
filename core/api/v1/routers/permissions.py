import fastapi
from fastapi import Depends, HTTPException, Body
from fastapi import Query
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User, Organization, Project
from core.schemas.permission import PermissionsResponse
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.project import IProjectService
from core.services.providers.organization import get_organization_service
from core.services.providers.permission import get_permission_service
from core.services.providers.project import get_project_service
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper

router = fastapi.APIRouter(prefix="/permissions", tags=["permissions"])

ALL_FIELDS = PermissionsResponse.model_fields.keys()


@router.get(
    path="/is-user-allowed-to-create-projects-inside-organization",
    response_model=bool,
    status_code=200,
)
@async_http_exception_mapper(

)
async def can_user_create_projects_inside_organization(
        org_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    org: Organization = (
        await organization_service.get_organization_by_id(
            org_id=org_id,
        )
    )
    if not org:
        return JSONResponse({'body': False})

    flag: bool = (
        await permission_service.can_user_create_projects_inside_organization(
            org_id=org_id,
            user_id=user.id,
        )
    )
    return JSONResponse({'body': flag})


@router.get(
    path="/is-user-allowed-to-edit-project",
    response_model=bool,
    status_code=200,
)
@async_http_exception_mapper(

)
async def can_user_edit_project(
        project_id: int = Query(),
        user: User = Depends(get_user),
        project_service: IProjectService = Depends(get_project_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    project: Project = (
        await project_service.get_project_by_id(
            project_id=project_id,
        )
    )
    if not project:
        return JSONResponse({'body': False})

    flag: bool = (
        await permission_service.can_user_edit_project(
            project_id=project_id,
            user_id=user.id,
        )
    )
    return JSONResponse({'body': flag})


@router.post(
    path="/is-user-allowed-to-edit-organization",
    response_model=bool,
)
@async_http_exception_mapper(

)
async def can_user_edit_organization(
        params: dict = Body(...),
        user: User = Depends(get_user),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    org_id = params.get("org_id")
    if not org_id:
        raise HTTPException(status_code=400, detail="Missing required parameter 'org_id'")

    result: bool = (
        await permission_service.can_user_edit_organization(
            user_id=user.id,
            org_id=org_id,
        )
    )
    return JSONResponse({'body': result})


@router.get(
    path="/is-user-allowed-to-create-organizations",
    response_model=bool,
)
@async_http_exception_mapper(

)
async def can_user_edit_organization(
        user: User = Depends(get_user),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    result: bool = (
        await permission_service.can_user_create_organizations(
            user_id=user.id,
        )
    )
    return JSONResponse({'body': result})

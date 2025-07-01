import fastapi
from fastapi import Depends, HTTPException
from fastapi import Query
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User, Organization, Project
from core.schemas.permission import PermissionsResponse
from core.services.domain.organization import OrganizationService
from core.services.domain.permission import PermissionService, get_permission_service
from core.services.domain.project import get_project_service, ProjectService
from core.services.interfaces.organization import IOrganizationService
#from core.services.providers.organization import get_organization_service
from core.services.providers.provider import get_organization_service

router = fastapi.APIRouter(prefix="/permissions", tags=["permissions"])

ALL_FIELDS = PermissionsResponse.model_fields.keys()


@router.get("/is-user-allowed-to-create-projects-inside-organization", response_model=bool)
async def can_user_create_projects_inside_organization(
        org_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: PermissionService = Depends(get_permission_service),
) -> JSONResponse:
    try:
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

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/is-user-allowed-to-edit-project", response_model=bool)
async def can_user_edit_project(
        project_id: int = Query(),
        user: User = Depends(get_user),
        project_service: ProjectService = Depends(get_project_service),
        permission_service: PermissionService = Depends(get_permission_service),
) -> JSONResponse:
    try:
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

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

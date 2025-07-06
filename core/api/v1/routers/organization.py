from idlelib.rpc import request_queue
from typing import Sequence

import fastapi
from fastapi import Body
from fastapi import Depends, Request
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse, Response

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.organization import OrganizationCreateInRequest, OrganizationDetailInfoResponse, OrganizationInPatch, \
    OrganizationShortInfoResponse, OrganizationInfoForEditResponse, OrganizationJoinRequest, \
    OrganizationId, OrganizationAndUserId, OrganizationMemberId
from core.schemas.organization_member import OrganizationMemberDetailInfo
from core.schemas.project import ProjectsInOrganizationShortInfoResponse
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.organization_member import IOrganizationMemberService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.project import IProjectService
from core.services.providers.organization import get_organization_service
from core.services.providers.organization_member import get_organization_member_service
from core.services.providers.permission import get_permission_service
from core.services.providers.project import get_project_service
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.logger import logger

router = fastapi.APIRouter(prefix="/org", tags=["organization"])


@router.post(
    path="/admin/members",
    response_model=Sequence[OrganizationMemberDetailInfo],
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def get_organization_members_for_admin(
        params: OrganizationId = Body(...),
        user: User = Depends(get_user),
        org_member_service: IOrganizationMemberService = Depends(get_organization_member_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    org_id = params.org_id

    await permission_service.raise_if_not_all([
        lambda: permission_service.can_user_edit_organization(user_id=user.id, org_id=org_id),
    ])

    # # Пользователь должен обладать правами на редактирование организации
    # flag = await permission_service.can_user_edit_organization(user_id=user.id, org_id=org_id)
    # if not flag: raise HTTPException(status_code=403, detail="Permission denied")

    result: Sequence[OrganizationMemberDetailInfo] = (
        await org_member_service.get_organization_members_for_admin(
            user_id=user.id,
            org_id=org_id,
        )
    )
    result = [i.model_dump() for i in result]

    return JSONResponse({'body': result})


@router.delete(
    path="/admin/members",
    status_code=204,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
    }
)
async def delete_organization_member_by_manager(
        params: OrganizationAndUserId = Body(...),
        user: User = Depends(get_user),
        org_member_service: IOrganizationMemberService = Depends(get_organization_member_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> Response:
    org_id = params.org_id
    user_id = params.user_id

    await permission_service.raise_if_not_all([
        lambda: permission_service.can_user_edit_organization(user_id=user.id, org_id=org_id),
    ])

    # # Пользователь должен обладать правами на редактирование организации
    # flag = await permission_service.can_user_edit_organization(user_id=user.id, org_id=org_id)
    # if not flag: raise HTTPException(status_code=403, detail="Permission denied")

    await org_member_service.delete_organization_member(
        user_id=user_id,
        org_id=org_id,
    )

    return Response(status_code=204)


@router.post(
    path="/join",
    response_model=OrganizationMemberId,
    status_code=201,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
        EntityAlreadyExists: (409, None),
    }
)
async def join_organization(
        params: OrganizationJoinRequest = Body(...),
        user: User = Depends(get_user),
        org_member_service: IOrganizationMemberService = Depends(get_organization_member_service),
) -> JSONResponse:
    result: OrganizationMemberId = (
        await org_member_service.join_organization(
            user_id=user.id,
            org_id=params.org_id,
            code=params.code,
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.get(
    path="/short-info",
    response_model=Sequence[OrganizationShortInfoResponse],
    status_code=200,
)
@async_http_exception_mapper(

)
async def get_all_organizations_short_info(
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    result: Sequence[OrganizationShortInfoResponse] = (
        await organization_service.get_all_organizations_with_short_info(
            user_id=user.id,
        )
    )
    result = [i.model_dump() for i in result]

    return JSONResponse({'body': result})


@router.get(
    path="/info-for-edit",
    response_model=OrganizationInfoForEditResponse,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def get_organization_info_for_edit_by_id(
        org_id: int = Query(..., ),
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    await permission_service.raise_if_not_all([
        lambda: permission_service.can_user_edit_organization(user_id=user.id, org_id=org_id),
    ])

    # # Пользователь должен обладать правами на редактирование организации
    # flag = await permission_service.can_user_edit_organization(user_id=user.id, org_id=org_id)
    # if not flag: raise HTTPException(status_code=403, detail="Permission denied")

    result: OrganizationInfoForEditResponse = (
        await organization_service.get_organization_info_for_edit(
            org_id=org_id,
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.get(
    path="/detail",
    response_model=OrganizationDetailInfoResponse,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def get_organization_detail_info_by_id(
        org_id: int = Query(..., ),
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    # Пользователь должен обладать правами на просмотр организации
    await permission_service.raise_if_not_all([
        lambda: permission_service.can_user_see_organization_detail(user_id=user.id, org_id=org_id),
    ])

    # flag = await permission_service.can_user_see_organization_detail(user_id=user.id, org_id=org_id)
    # if not flag:
    #     logger.warning(f"User {user.id} tried to access organization {org_id} without permission")
    #     raise HTTPException(status_code=403, detail="Not allowed")

    result: OrganizationDetailInfoResponse = (
        await organization_service.get_organization_detail_info_by_id(
            org_id=org_id,
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.post(
    path="/",
    response_model=OrganizationId,
    status_code=201,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
    }
)
async def create_organization(
        params: OrganizationCreateInRequest = Body(...),
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    # Пользователь должен обладать правами на создание организаций
    await permission_service.raise_if_not_all([
        lambda: permission_service.can_user_create_organizations(user_id=user.id),
    ])

    # flag = await permission_service.can_user_create_organizations(user_id=user.id)
    # if not flag: raise HTTPException(status_code=403, detail="Not allowed")

    result: OrganizationId = (
        await organization_service.create_organization(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.patch(
    path="/",
    response_model=OrganizationId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def patch_organization(
        params: OrganizationInPatch = Body(..., ),
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    # Пользователь должен иметь права на редактирование организации
    await permission_service.raise_if_not_all([
        lambda: permission_service.can_user_edit_organization(user_id=user.id, org_id=params.org_id),
    ])

    # flag = await permission_service.can_user_edit_organization(user_id=user.id, org_id=params.org_id)
    # if not flag: raise HTTPException(status_code=403, detail="Not allowed")

    result: OrganizationId = (
        await organization_service.patch_organization_by_id(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({"body": result})


@router.get(
    path="/projects-short-info",
    response_model=Sequence[ProjectsInOrganizationShortInfoResponse],
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def get_organization_projects_short_info(
        org_id: int = Query(),
        user: User = Depends(get_user),
        project_service: IProjectService = Depends(get_project_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    # Пользователь должен обладать правами на просмотр организации
    await permission_service.raise_if_not_all([
        lambda: permission_service.can_user_see_organization_detail(user_id=user.id, org_id=org_id),
    ])

    # flag = await permission_service.can_user_see_organization_detail(user_id=user.id, org_id=org_id)
    # if not flag: raise HTTPException(status_code=403, detail="Not allowed")

    result: Sequence[ProjectsInOrganizationShortInfoResponse] = (
        await project_service.get_projects_short_info_in_organization(
            user_id=user.id,
            org_id=org_id,
        )
    )
    result = [i.model_dump() for i in result]

    return JSONResponse({"body": result})

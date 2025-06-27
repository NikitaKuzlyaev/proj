from typing import Sequence

import fastapi
from fastapi import Body
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user, oauth2_scheme
from core.dependencies.repository import get_repository
from core.models import User, Organization, Project
from core.models.organizationMember import OrganizationMember
# from core.repository.crud.folder import FolderCRUDRepository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.organization import OrganizationCreateInRequest, OrganizationResponse, SequenceOrganizationResponse, \
    OrganizationDetailInfoResponse, OrganizationInPatch, SequenceAllOrganizationsShortInfoResponse, \
    OrganizationShortInfoResponse, OrganizationInDelete, OrganizationInfoForEditResponse, OrganizationVisibilityType, \
    OrganizationJoinPolicyType, OrganizationActivityStatusType, OrganizationProjectsShortInfoResponse
# from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.user import UserCRUDRepository
from core.schemas.project import ProjectsInOrganizationRequest, ProjectManagerInfo
from core.services.domain.project import ProjectService, get_project_service
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)
from core.services.domain.permission import PermissionService, get_permission_service

router = fastapi.APIRouter(prefix="/org", tags=["organization"])

# from core.services.domain import organization as organization_service
from core.services.domain.organization import get_organization_service, OrganizationService
from templates import templates

"""
    ----------------------------------------------------------
"""


@router.get("/", response_class=JSONResponse)
async def get_all_organizations(
        request: Request,
        response: Response,
        organization_service: OrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    try:
        orgs: Sequence[Organization] = await organization_service.get_all_organizations()

        org_response = SequenceOrganizationResponse.model_validate({"body": orgs})
        content = org_response.model_dump()

        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all-short-info", response_class=JSONResponse)
async def get_all_organizations_short_info(
        request: Request,
        response: Response,
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    try:
        orgs: Sequence[OrganizationShortInfoResponse] = \
            await organization_service.get_all_organizations_with_short_info(
                user=user,
            )

        org_response = SequenceAllOrganizationsShortInfoResponse.model_validate({"body": orgs})
        content = org_response.model_dump()

        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/info", response_class=JSONResponse)
async def get_organization_info_by_id(
        request: Request,
        response: Response,
        org_id: int,
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    try:

        org: Organization = await organization_service.get_organization_by_id(
            org_id=org_id,
        )
        org_response = OrganizationResponse(
            id=org.id,
            name=org.name,
            short_description=org.short_description,
            long_description=org.long_description,
            creator_id=org.creator_id,
        )
        content = org_response.model_dump()
        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/info-for-edit", response_model=OrganizationInfoForEditResponse)
async def get_organization_info_for_edit_by_id(
        request: Request,
        response: Response,
        org_id: int,
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        permission_service: PermissionService = Depends(get_permission_service),
) -> JSONResponse:
    try:
        org: Organization = await organization_service.get_organization_by_id(
            org_id=org_id,
        )
        # check permissions
        allow_user_edit: bool = \
            await permission_service.can_user_edit_organization(
                user_id=user.id,
                org_id=org.id,
            )

        org_response = OrganizationInfoForEditResponse(
            id=org.id,
            name=org.name,
            short_description=org.short_description,
            long_description=org.long_description,
            visibility=OrganizationVisibilityType(org.visibility),
            activity_status=OrganizationActivityStatusType(org.activity_status),
            join_policy=OrganizationJoinPolicyType(org.join_policy),
        )
        content = org_response.model_dump()
        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/detail", response_model=OrganizationDetailInfoResponse)
async def get_organization_detail_info_by_id(
        request: Request,
        response: Response,
        org_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        permission_service: PermissionService = Depends(get_permission_service),
) -> JSONResponse:
    try:
        org: Organization = \
            await organization_service.get_organization_by_id(
                org_id=org_id
            )

        if not org:
            raise HTTPException(status_code=404)

        org_members: Sequence[OrganizationMember] = \
            await organization_service.get_organization_members_by_org_id(
                org_id=org_id
            )

        number_of_members = len(org_members)

        # check permissions
        allow_user_edit: bool = \
            await permission_service.can_user_edit_organization(
                user_id=user.id,
                org_id=org.id,
            )

        org_response = OrganizationDetailInfoResponse(
            id=org.id,
            name=org.name,
            short_description=org.short_description,
            long_description=org.long_description,
            creator_id=org.creator_id,
            created_at=org.created_at.isoformat(),
            number_of_members=len(org_members),
            allow_user_edit=allow_user_edit,
            allow_user_delete=(user.id == org.creator_id),
        )
        content = org_response.model_dump()
        return JSONResponse(content=content)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_class=JSONResponse)
async def create_organization(
        request: Request,
        response: Response,
        user: User = Depends(get_user),
        org_create_in_request_schema: OrganizationCreateInRequest = Body(...),
        organization_service: OrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    try:
        org = await organization_service.create_organization(
            org_create_in_request_schema=org_create_in_request_schema,
            user=user,
        )
        org_response = OrganizationResponse.model_validate(org)
        return JSONResponse(content=org_response.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/", response_class=JSONResponse)
async def patch_organization(
        request: Request,
        response: Response,
        org_patch_form: OrganizationInPatch,
        user: User = Depends(get_user),
        organization_service: OrganizationService = Depends(get_organization_service),
        permission_service: PermissionService = Depends(get_permission_service),
) -> JSONResponse:
    # check permissions
    flag: bool = \
        await permission_service.can_user_edit_organization(
            user_id=user.id,
            org_id=org_patch_form.id,
        )
    if not flag:
        raise HTTPException(status_code=400, detail="Not allowed")

    org: Organization = \
        await organization_service.patch_organization_by_id(
            org_id=org_patch_form.id,
            name=org_patch_form.name,
            short_description=org_patch_form.short_description,
            long_description=org_patch_form.long_description,
            visibility=org_patch_form.visibility,
            activity_status=org_patch_form.activity_status,
            join_policy=org_patch_form.join_policy,
        )
    if not org:
        raise HTTPException(status_code=404)

    return JSONResponse({"message": "its ok"})


@router.get("/projects-short-info", response_model=Sequence[OrganizationProjectsShortInfoResponse])
async def get_organization_projects_short_info(
        request: Request,
        response: Response,
        #projects_in_org_schema: ProjectsInOrganizationRequest,
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
            raise HTTPException(status_code=404)

        projects: Sequence[Project] = \
            await project_service.get_all_projects_in_organization_by_org_id(
                org_id=org.id
            )

        res = [
            OrganizationProjectsShortInfoResponse(
                id=project.id,
                name=project.name,
                short_description=project.short_description,
                manager=ProjectManagerInfo(
                    user_id=user.id,
                    name=user.username,
                    avatar=''
                ),
                team_current_size=0,
                team_full_size=0,
                open_vacancies=0
            ).model_dump() for project in projects
        ]

        return JSONResponse({'body': res})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



#
# @router.delete("/", response_class=HTMLResponse)
# async def delete_organization(
#         request: Request,
#         response: Response,
#         org_delete_form: OrganizationInDelete,
#         user: User = Depends(get_user),
#         organization_service: OrganizationService = Depends(get_organization_service),
#         permission_service: PermissionService = Depends(get_permission_service),
# ) -> JSONResponse:
#
#     org: bool = await organization_service.delete_organization(org=org_delete_form.id, user=user)
#     if not org:
#
#     flag: bool = \
#         await permission_service.can_user_edit_organization(
#             user_id=user.id,
#             org_id=org_patch_form.id,
#         )
#
#     if not flag:
#         raise HTTPException(status_code=400, detail="Not allowed")
#
#     org: Organization = \
#         await organization_service.patch_organization_by_id(
#             org_id=org_patch_form.id,
#             name=org_patch_form.name,
#             short_description=org_patch_form.short_description,
#             long_description=org_patch_form.long_description,
#         )
#
#     if not org:
#         raise HTTPException(status_code=404)
#
#     return JSONResponse({"message": "its ok"})

"""
    ----------------------------------------------------------
"""

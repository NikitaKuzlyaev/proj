from typing import Sequence

import fastapi
from fastapi import Body
from fastapi import Depends
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User, Organization, Project
from core.models.organizationMember import OrganizationMember
from core.schemas.organization import OrganizationCreateInRequest, OrganizationResponse, SequenceOrganizationResponse, \
    OrganizationDetailInfoResponse, OrganizationInPatch, SequenceAllOrganizationsShortInfoResponse, \
    OrganizationShortInfoResponse, OrganizationInfoForEditResponse, OrganizationVisibilityType, \
    OrganizationJoinPolicyType, OrganizationActivityStatusType, OrganizationJoinResponse, OrganizationJoinRequest, \
    OrganizationMembersForAdminRequest
from core.schemas.organization_member import OrganizationMemberForAdminResponse, OrganizationMemberDetailInfo, \
    OrganizationMemberDeleteResponse
from core.schemas.project import ProjectManagerInfo, ProjectsInOrganizationShortInfoResponse
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.organization_member import IOrganizationMemberService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.project import IProjectService
from core.services.providers.organization import get_organization_service
from core.services.providers.organization_member import get_organization_member_service
from core.services.providers.permission import get_permission_service
from core.services.providers.project import get_project_service

router = fastapi.APIRouter(prefix="/org", tags=["organization"])


@router.post("/admin/members", response_model=Sequence[OrganizationMemberDetailInfo])
async def get_organization_members_for_admin(
        params: OrganizationMembersForAdminRequest = Body(...),
        user: User = Depends(get_user),
        org_member_service: IOrganizationMemberService = Depends(get_organization_member_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    org_id = params.org_id

    # Пользователь должен обладать правами на редактирование организации
    flag = await permission_service.can_user_edit_organization(user_id=user.id, org_id=org_id)
    if not flag: raise HTTPException(status_code=403, detail="Permission denied")

    try:
        result: Sequence[OrganizationMemberDetailInfo] = (
            await org_member_service.get_organization_members_for_admin(
                user_id=user.id,
                org_id=org_id,
            )
        )
        result = [i.model_dump() for i in result]
        return JSONResponse({'body': result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/admin/members")
async def delete_organization_member_by_manager(
        params: dict = Body(...),
        user: User = Depends(get_user),
        org_member_service: IOrganizationMemberService = Depends(get_organization_member_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    """
    """
    org_id = params.get("org_id")
    user_id = params.get("user_id")
    if not org_id or not user_id or type(org_id) != int or type(user_id) != int:
        raise HTTPException(status_code=404, detail="Organization not found")

    flag = await permission_service.can_user_edit_organization(user_id=user.id, org_id=org_id)
    if not flag:
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        result: OrganizationMemberDeleteResponse = (
            await org_member_service.delete_organization_member(
                user_id=user_id,
                org_id=org_id,
            )
        )
        result = result.model_dump()
        return JSONResponse({'body': result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/join", response_class=JSONResponse)
async def join_organization(
        org_join_request: OrganizationJoinRequest = Body(...),
        user: User = Depends(get_user),
        org_member_service: IOrganizationMemberService = Depends(get_organization_member_service),
) -> JSONResponse:
    """

    Args:
        org_join_request:
        user:
        org_member_service:

    Returns:

    """
    try:
        result: OrganizationJoinResponse = (
            await org_member_service.join_organization(
                user_id=user.id,
                org_id=org_join_request.org_id,
            )
        )
        result = result.model_dump()
        return JSONResponse({'body': result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_class=JSONResponse)
async def get_all_organizations(
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    try:
        orgs: Sequence[Organization] = (
            await organization_service.get_all_organizations()
        )
        org_response = SequenceOrganizationResponse.model_validate({"body": orgs})
        content = org_response.model_dump()
        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/short-info", response_class=JSONResponse)
async def get_all_organizations_short_info(
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    try:
        orgs: Sequence[OrganizationShortInfoResponse] = \
            await organization_service.get_all_organizations_with_short_info(
                user_id=user.id,
            )

        org_response = SequenceAllOrganizationsShortInfoResponse.model_validate({"body": orgs})
        content = org_response.model_dump()

        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/info", response_class=JSONResponse)
async def get_organization_info_by_id(
        org_id: int,
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    try:
        org: Organization = (
            await organization_service.get_organization_by_id(
                org_id=org_id,
            )
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
        org_id: int,
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    try:
        org: Organization = (
            await organization_service.get_organization_by_id(
                org_id=org_id,
            )
        )
        allow_user_edit: bool = (
            await permission_service.can_user_edit_organization(
                user_id=user.id,
                org_id=org.id,
            )
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
        org_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    can_user_see_organization_detail: bool = (
        await permission_service.can_user_see_organization_detail(
            user_id=user.id,
            org_id=org_id,
        )
    )
    if not can_user_see_organization_detail:
        raise HTTPException(status_code=403, detail="Not allowed")

    try:
        org: Organization = (
            await organization_service.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise HTTPException(status_code=404)

        org_members: Sequence[OrganizationMember] = (
            await organization_service.get_organization_members_by_org_id(
                user_id=user.id,
                org_id=org_id,
            )
        )

        number_of_members = len(org_members)

        org_response = OrganizationDetailInfoResponse(
            id=org.id,
            name=org.name,
            short_description=org.short_description,
            long_description=org.long_description,
            creator_id=org.creator_id,
            created_at=org.created_at.isoformat(),
            number_of_members=len(org_members),
        )
        content = org_response.model_dump()
        return JSONResponse(content=content)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_class=JSONResponse)
async def create_organization(
        user: User = Depends(get_user),
        org_create_in_request_schema: OrganizationCreateInRequest = Body(...),
        organization_service: IOrganizationService = Depends(get_organization_service),
) -> JSONResponse:
    try:
        org: Organization = (
            await organization_service.create_organization(
                user_id=user.id,
                **org_create_in_request_schema.model_dump(),
            )
        )
        org_response = OrganizationResponse.model_validate(org)
        return JSONResponse(content=org_response.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/", response_class=JSONResponse)
async def patch_organization(
        org_patch_form: OrganizationInPatch,
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:

    # Пользователь должен иметь права на редактирование организации
    flag = await permission_service.can_user_edit_organization(user_id=user.id, org_id=org_patch_form.org_id)
    if not flag: raise HTTPException(status_code=403, detail="Not allowed")

    org: Organization | None = (
        await organization_service.patch_organization_by_id(
            user_id=user.id,
            org_id=org_patch_form.org_id,
            name=org_patch_form.name,
            short_description=org_patch_form.short_description,
            long_description=org_patch_form.long_description,
            visibility=org_patch_form.visibility,
            activity_status=org_patch_form.activity_status,
            join_policy=org_patch_form.join_policy,
        )
    )
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return JSONResponse({"body": {'org_id': org.id}})


@router.get("/projects-short-info", response_model=Sequence[ProjectsInOrganizationShortInfoResponse])
async def get_organization_projects_short_info(
        org_id: int = Query(),
        user: User = Depends(get_user),
        organization_service: IOrganizationService = Depends(get_organization_service),
        project_service: IProjectService = Depends(get_project_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    try:
        org: Organization = \
            await organization_service.get_organization_by_id(
                org_id=org_id
            )
        if not org:
            raise HTTPException(status_code=404)

        res: Sequence[ProjectsInOrganizationShortInfoResponse] = (
            await project_service.get_projects_short_info_in_organization(
                user_id=user.id,
                org_id=org_id,
            )
        )
        res = [i.model_dump() for i in res]
        return JSONResponse({"body": res})

        # projects: Sequence[Project] = \
        #     await project_service.get_all_projects_in_organization_by_org_id(
        #         user_id=user.id,
        #         org_id=org.id
        #     )
        #
        # res = [
        #     OrganizationProjectsShortInfoResponse(
        #         id=project.id,
        #         name=project.name,
        #         short_description=project.short_description,
        #         manager=ProjectManagerInfo(
        #             user_id=project.creator_id,
        #             name=user.username,
        #             avatar=''
        #         ),
        #         team_current_size=0,
        #         team_full_size=0,
        #         open_vacancies=0
        #     ).model_dump() for project in projects
        # ]

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

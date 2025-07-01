# # core/services/providers/organization_member.py
#
# # core/services/providers/organization.py
# from fastapi import Depends
#
# from core.dependencies.repository import get_repository
# from core.repository.crud.organization import OrganizationCRUDRepository
# from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
# from core.repository.crud.permission import PermissionCRUDRepository
# from core.services.domain.organization import OrganizationService
# from core.services.domain.organization_member import OrganizationMemberService
# from core.services.domain.user import UserService, get_user_service
# from core.services.interfaces.organization import IOrganizationService
# from core.services.interfaces.organization_member import IOrganizationMemberService
# #from core.services.providers.organization import get_organization_service
#
#
#
# class Provider:
#
#     def __init__(
#             self,
#     ):
#         ...
#
#
#     def get_organization_member_service(
#             self,
#             org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
#             member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
#             permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
#             user_service: UserService = Depends(get_user_service),
#             org_service: IOrganizationService = Depends(get_organization_service),
#     ) -> IOrganizationMemberService:
#         return OrganizationMemberService(
#             org_repo=org_repo,
#             member_repo=member_repo,
#             permission_repo=permission_repo,
#             user_service=user_service,
#             org_service=org_service,
#         )
#
#     def get_organization_service(
#             self,
#             org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
#             member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
#             permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
#             # user_service: UserService = Depends(get_user_service),
#             org_member_service: IOrganizationMemberService = Depends(get_organization_member_service),
#     ) -> IOrganizationService:
#         return OrganizationService(
#             org_repo=org_repo,
#             member_repo=member_repo,
#             permission_repo=permission_repo,
#             # user_service=user_service,
#             org_member_service=org_member_service,
#         )
#
#
# async def get_provider():
#     return Provider()
#
#
# async def get_organization_service(provider: Provider = Depends(get_provider)):
#     res = await provider.get_organization_service()
#

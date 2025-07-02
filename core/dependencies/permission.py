# from fastapi import Depends
#
# from core.dependencies.authorization import get_user
# from core.models import User
# from core.services.interfaces.permission import IPermissionService
# from core.services.providers.permission import get_permission_service
#
#
# def require_permission(*args: str) -> bool:
#     async def dependency(
#         user: User = Depends(get_user),
#         permission_service: IPermissionService = Depends(get_permission_service),
#         org_id: int = Depends(get_org_id_from_params),
#     ):
#         if not await permission_service.has_permission(user.id, permission, org_id):
#             raise HTTPException(status_code=403, detail=f"Permission '{permission}' denied")
#
#     return Depends(dependency)

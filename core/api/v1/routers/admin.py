import fastapi
from fastapi import Depends
from fastapi import HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.admin import AdminPermissionSignature
from core.services.interfaces.admin import IAdminService
from core.services.interfaces.permission import IPermissionService
from core.services.providers.admin import get_admin_service
from core.services.providers.permission import get_permission_service
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper

router = fastapi.APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    path="/sign",
    response_model=AdminPermissionSignature,
    status_code=200,
)
@async_http_exception_mapper(

)
async def admin_panel(
        user: User = Depends(get_user),
        admin_service: IAdminService = Depends(get_admin_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    # Пользователь должен иметь админ-права
    flag = await permission_service.is_user_admin(user_id=user.id)
    if not flag: raise HTTPException(status_code=403, detail="Not allowed")

    result = AdminPermissionSignature(
        permission_id=-1,
        sign=True
    )
    result = result.model_dump()
    return JSONResponse({'body': result})

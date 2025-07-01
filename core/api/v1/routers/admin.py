import fastapi
from fastapi import Depends
from fastapi import HTTPException
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.admin import AdminPermissionSignature
from core.services.interfaces.admin import IAdminService
from core.services.providers.admin import get_admin_service

router = fastapi.APIRouter(prefix="/admin", tags=["admin"])


@router.get("/sign", response_model=AdminPermissionSignature)
async def admin_panel(
        user: User = Depends(get_user),
        admin_service: IAdminService = Depends(get_admin_service),
) -> JSONResponse:
    try:
        res: AdminPermissionSignature = (
            await admin_service.base_admin_check(
                user_id=user.id
            )
        )
        res = res.model_dump()
        return JSONResponse({'body': res})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

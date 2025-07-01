from typing import Sequence

import fastapi
from fastapi import Depends, Body
from fastapi import Query, HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.admin import AdminPermissionSignature
from core.schemas.project import ProjectCreateRequest, ProjectFullInfoResponse, ProjectPatchRequest, \
    ProjectVacanciesShortInfoResponse, CreatedProjectResponse, PatchedProjectResponse
from core.services.admin.admin import AdminService, get_admin_service
from core.services.domain.project import  ProjectService
from core.services.domain.vacancy import VacancyService, get_vacancy_service

router = fastapi.APIRouter(prefix="/admin", tags=["admin"])


@router.get("/sign", response_model=AdminPermissionSignature)
async def admin_panel(
        user: User = Depends(get_user),
        admin_service: AdminService = Depends(get_admin_service),
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



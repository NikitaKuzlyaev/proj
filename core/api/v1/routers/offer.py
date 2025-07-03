import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User

router = fastapi.APIRouter(prefix="/offer", tags=["offer"])


@router.get("/")
async def get____(
        user: User = Depends(get_user),
) -> JSONResponse:
    ...

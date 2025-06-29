import fastapi
from fastapi import Depends
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm

from core.dependencies.authorization import oauth2_scheme
from core.dependencies.repository import get_repository
from core.models import User
from core.repository.crud.user import UserCRUDRepository
from core.schemas.user import UserCreate, UserOut, Token
from core.services.domain import auth as auth_service

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserOut)
async def register(
        data: UserCreate,
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
):
    user: User = (
        await auth_service.register_user(
            data=data,
            user_repo=user_repo,
        )
    )
    return user


@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
):
    token: str = (
        await auth_service.authenticate_user(
            username=form_data.username,
            password=form_data.password,
            user_repo=user_repo,
        )
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/get-my-token")
async def get_my_token(
        token: str = Security(oauth2_scheme),
):
    return token

import datetime

import pydantic
from jose import jwt as jose_jwt, JWTError as JoseJWTError

from core.models.user import User
from core.schemas.jwt import JWTAccount, JWToken
from core.utilities.exceptions.auth import UndecodedToken, InvalidToken, TokenException
from core.utilities.exceptions.database import EntityDoesNotExist

JWT_SECRET_KEY = "super-dupper-secret-key"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRATION_TIME = 1  # в минутах
JWT_SUBJECT = "i am"
JWT_MIN = 1


class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
            self, *,
            jwt_data: dict[str, str],
            expires_delta: datetime.timedelta | None = None,
    ) -> str:
        """
        """
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_MIN)

        to_encode = jwt_data.copy()
        to_encode.update(JWToken(exp=expire, sub=JWT_SUBJECT).dict())
        res = jose_jwt.encode(to_encode, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return res

    def generate_access_token(
            self,
            account: User
    ) -> str:
        """
        """
        if not account:
            raise EntityDoesNotExist(f"Cannot generate JWT token for without Account entity!")

        res = self._generate_jwt_token(
            jwt_data=JWTAccount(username=account.username).dict(),
            expires_delta=datetime.timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRATION_TIME),
        )

        return res

    def retrieve_details_from_token(
            self,
            token: str,
            secret_key: str = JWT_SECRET_KEY
    ) -> dict[str, str]:
        """
        """
        try:
            payload = jose_jwt.decode(token=token, key=secret_key, algorithms=[JWT_ALGORITHM])
            jwt_account = JWTAccount(username=payload["username"])

        except JoseJWTError as token_decode_error:
            raise UndecodedToken("Unable to decode JWT Token") from token_decode_error
        except pydantic.ValidationError as validation_error:
            raise InvalidToken("Invalid payload in token") from validation_error
        except:
            raise TokenException

        res = {
            "username": jwt_account.username,
        }

        return res


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()

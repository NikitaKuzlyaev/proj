from typing import Protocol

from core.models import User
from core.utilities.loggers.log_decorator import log_calls


class IUserService(Protocol):

    @log_calls
    async def get_user_by_id(
            self,
            user_id: int,
    ) -> User:
        ...

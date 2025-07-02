from core.models import Permission

from core.schemas.permission import PermissionsShortResponse
from core.utilities.loggers.log_decorator import log_calls


class PermissionMapper:
    def __init__(
            self,
    ):
        return

    @log_calls
    def get_short_permission_response(
            self,
            permission: Permission,
    ) -> PermissionsShortResponse:
        res = PermissionsShortResponse(
            permission_id=permission.id,
        )
        return res


def get_permission_mapper(
) -> PermissionMapper:
    return PermissionMapper()

from core.models import Permission

from core.schemas.permission import PermissionsShortResponse


class PermissionMapper:
    def __init__(
            self,
    ):
        return

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

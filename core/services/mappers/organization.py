from core.models import Project, Organization

from core.models.user import User
from core.schemas.organization import OrganizationInfoForEditResponse, OrganizationVisibilityType, \
    OrganizationActivityStatusType, OrganizationJoinPolicyType
from core.schemas.project import ProjectFullInfoResponse, ProjectManagerInfo, ProjectVisibilityType, \
    ProjectActivityStatusType, CreatedProjectResponse, PatchedProjectResponse
from core.utilities.loggers.log_decorator import log_calls


class OrganizationMapper:
    def __init__(
            self,
    ):
        return

    @log_calls
    def compile_organization_info_for_edit(
            self,
            org: Organization,
    ) -> OrganizationInfoForEditResponse:
        res = OrganizationInfoForEditResponse(
            id=org.id,
            name=org.name,
            short_description=org.short_description,
            long_description=org.long_description,
            visibility=OrganizationVisibilityType(org.visibility),
            activity_status=OrganizationActivityStatusType(org.activity_status),
            join_policy=OrganizationJoinPolicyType(org.join_policy),
        )
        return res


def get_org_mapper(
) -> OrganizationMapper:
    return OrganizationMapper()

from core.models import Project

from core.models.user import User
from core.schemas.project import ProjectFullInfoResponse, ProjectManagerInfo, ProjectVisibilityType, \
    ProjectActivityStatusType, CreatedProjectResponse, PatchedProjectResponse


class ProjectMapper:
    def __init__(
            self,
    ):
        return

    def get_project_full_info_response(
            self,
            project: Project,
            manager: User,
    ) -> ProjectFullInfoResponse:
        res = ProjectFullInfoResponse(
            org_id=project.organization_id,
            name=project.name,
            short_description=project.short_description,
            long_description=project.long_description,
            manager=ProjectManagerInfo(
                user_id=manager.id,
                name=manager.username,
                avatar=''
            ),
            visibility=ProjectVisibilityType(project.visibility),
            activity_status=ProjectActivityStatusType(project.activity_status),
            team_current_size=0,
            team_full_size=0,
            open_vacancies=0
        )
        return res

    def get_created_project_response(
            self,
            project: Project,
    ) -> CreatedProjectResponse:
        res = CreatedProjectResponse(
            project_id=project.id,
        )
        return res

    def get_patched_project_response(
            self,
            project: Project,
    ) -> PatchedProjectResponse:
        res = PatchedProjectResponse(
            project_id=project.id,
        )
        return res


def get_project_mapper(
) -> ProjectMapper:
    return ProjectMapper()

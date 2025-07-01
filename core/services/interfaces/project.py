from typing import Sequence, Protocol

from core.models import Project
from core.models.user import User
from core.schemas.project import ProjectFullInfoResponse, CreatedProjectResponse, PatchedProjectResponse


class IProjectService(Protocol):

    async def get_all_projects_in_organization_by_org_id(
            self,
            user_id: int,
            org_id: int,
    ) -> Sequence[Project]:
        """
        ???

        Args:
            user_id:
            org_id:

        Returns:
            Sequence[Project]
        """
        ...

    async def get_project_by_id(
            self,
            project_id: int,
    ) -> Project:
        """
        ???

        Args:
            project_id:

        Returns:
            Project
        """
        ...

    async def get_project_full_info_response(
            self,
            user_id: int,
            project_id: int,
    ) -> ProjectFullInfoResponse:
        """
        ???

        Args:
            user_id:
            project_id:

        Returns:
            ProjectFullInfoResponse
        """
        ...

    async def create_project(
            self,
            user_id: int,
            name: str,
            org_id: int,
            short_description: str,
            long_description: str,
            activity_status: str,
            visibility: str,
    ) -> CreatedProjectResponse:
        """
        ???

        Args:
            user_id:
            name:
            org_id:
            short_description:
            long_description:
            activity_status:
            visibility:

        Returns:
            CreatedProjectResponse
        """
        ...

    async def patch_project(
            self,
            user_id: int,
            project_id: int,
            name: str,
            org_id: int,
            short_description: str,
            long_description: str,
            activity_status: str,
            visibility: str,
    ) -> PatchedProjectResponse:
        """
        ???

        Args:
            user_id:
            project_id:
            name:
            org_id:
            short_description:
            long_description:
            activity_status:
            visibility:

        Returns:
            PatchedProjectResponse
        """
        ...

    async def get_project_creator(
            self,
            project_id: int,
    ) -> User | None:
        """
        ???

        Args:
            project_id:

        Returns:
            User | None
        """
        ...

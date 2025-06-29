from typing import Sequence

from sqlalchemy import select, update

from core.dependencies.repository import get_repository
from core.models import Project
from core.models.user import User
from core.repository.crud.base import BaseCRUDRepository


class ProjectCRUDRepository(BaseCRUDRepository):

    async def get_all_projects(
            self,
    ) -> Sequence[Project]:
        result = await self.async_session.execute(select(Project))
        projects = result.scalars().all()
        return projects

    async def get_all_projects_in_organization_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[Project]:
        stmt = select(Project).where(Project.organization_id == org_id)
        result = await self.async_session.execute(stmt)
        projects = result.scalars().all()
        return projects

    async def get_project_by_id(
            self,
            project_id: int,
    ) -> Project:
        stmt = select(Project).where(Project.id == project_id)
        result = await self.async_session.execute(stmt)
        project = result.scalars().one_or_none()
        return project

    async def get_project_creator(
            self,
            project_id: int,
    ) -> User | None:
        project: Project = await self.get_project_by_id(project_id=project_id)

        stmt = select(User).where(User.id == project.creator_id)
        result = await self.async_session.execute(stmt)
        user = result.scalars().one_or_none()
        return user

    async def patch_project_by_id(
            self,
            project_id: int,
            org_id: int,
            name: str,
            short_description: str,
            long_description: str,
            visibility: str,
            activity_status: str
    ) -> Project | None:
        stmt = (
            update(
                Project
            )
            .where(
                Project.id == project_id
            )
            .values(
                organization_id=org_id,
                name=name,
                short_description=short_description,
                long_description=long_description,
                visibility=visibility,
                activity_status=activity_status
            )
            .execution_options(
                synchronize_session="fetch"
            )
        )

        await self.async_session.execute(stmt)
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def create_project(
            self,
            org_id: int,
            user_id: int,
            name: str,
            short_description: str,
            long_description: str,
            activity_status: str,
            visibility: str,
    ) -> Project:
        new_project: Project = Project(
            name=name,
            creator_id=user_id,
            organization_id=org_id,
            short_description=short_description,
            long_description=long_description,
            activity_status=activity_status,
            visibility=visibility
        )

        self.async_session.add(instance=new_project)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_project)

        return new_project


project_repo = get_repository(repo_type=ProjectCRUDRepository)

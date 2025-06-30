from typing import Sequence

from sqlalchemy import select, update

from core.dependencies.repository import get_repository
from core.models import Project
from core.models.user import User
from core.repository.crud.base import BaseCRUDRepository


class ProjectCRUDRepository(BaseCRUDRepository):

    async def get_all_projects(
            self,
    ) -> Sequence[Project] | None:
        """
        Получить все объекты Project
        :return: последовательность объектов Project или None
        """
        result = await self.async_session.execute(
            select(
                Project
            )
        )
        projects = result.scalars().all()
        return projects

    async def get_all_projects_in_organization_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[Project] | None:
        """
        Получить все Project с Project.organization_id == org_id
        :param org_id: id объекта Organization
        :return: последовательность объектов Project или None
        """
        result = await self.async_session.execute(
            select(
                Project
            ).where(
                Project.organization_id == org_id
            )
        )
        projects = result.scalars().all()
        return projects

    async def get_project_by_id(
            self,
            project_id: int,
    ) -> Project | None:
        """
        Получить Project по его id
        :param project_id: id искомого объекта Project
        :return: объект Project или None
        """
        result = await self.async_session.execute(
            select(
                Project
            ).where(
                Project.id == project_id
            )
        )
        project = result.scalars().one_or_none()
        return project

    async def get_project_creator(
            self,
            project_id: int,
    ) -> User | None:
        """
        Получить User указанного как создателя Project
        :param project_id: id объекта Project
        :return: объект User или None
        """
        project: Project = await self.get_project_by_id(project_id=project_id)
        result = await self.async_session.execute(
            select(
                User
            ).where(
                User.id == project.creator_id
            )
        )
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
        """
        Обновить поля объекта Project в соответствии с указанными в параметрах
        :param project_id: id объекта Project
        :param org_id: id объекта Organization
        :param name: название
        :param short_description: короткое описание
        :param long_description: длинное описание
        :param visibility: тип видимости (str, Enum)
        :param activity_status: тип активности (str, Enum)
        :return: обновленный объект Project или None
        """
        await self.async_session.execute(
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
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(
                Project
            ).where(
                Project.id == project_id
            )
        )
        return result.scalar_one_or_none()

    async def create_project(
            self,
            user_id: int,
            org_id: int,
            name: str,
            short_description: str,
            long_description: str,
            activity_status: str,
            visibility: str,
    ) -> Project:
        """
        Создать объект Project с полями указанными в параметрах
        :param user_id: id объекта User (создатель Project)
        :param org_id: id объекта Organization
        :param name: название
        :param short_description: короткое описание
        :param long_description: длинное описание
        :param visibility: тип видимости (str, Enum)
        :param activity_status: тип активности (str, Enum)
        :return: созданный объект Project
        """
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


project_repo = get_repository(
    repo_type=ProjectCRUDRepository
)

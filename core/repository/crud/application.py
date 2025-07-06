from typing import Sequence, Tuple

from sqlalchemy import select, update, Row

from core.dependencies.repository import get_repository
from core.models import Project
from core.models.application import Application
from core.models.permissions import Permission, PermissionType, ResourceType
from core.models.vacancy import Vacancy
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.application import ApplicationActivityStatusType, ApplicationMainInfo
from core.utilities.loggers.log_decorator import log_calls


class ApplicationCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def create_application(
            self,
            user_id: int,
            vacancy_id: int,
            description: str,
            activity_status: str,
    ) -> Application:
        new_application = Application(
            user_id=user_id,
            vacancy_id=vacancy_id,
            description=description,
            activity_status=activity_status,
        )
        self.async_session.add(instance=new_application)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_application)
        return new_application

    @log_calls
    async def patch_application(
            self,
            application_id: int,
            description: str,
            activity_status: str,
    ) -> Application | None:
        await self.async_session.execute(
            update(
                Application
            ).where(
                Application.id == application_id,
            ).values(
                description=description,
                activity_status=activity_status,
            )
        )
        await self.async_session.commit()
        application = await self.async_session.execute(
            select(
                Application
            ).where(
                Application.id == application_id,
            )
        )
        return application.scalar_one_or_none()

    @log_calls
    async def get_application_by_id(
            self,
            application_id: int,
    ) -> Application | None:
        application = await self.async_session.execute(
            select(
                Application
            ).where(
                Application.id == application_id,
            )
        )
        return application.scalar_one_or_none()

    @log_calls
    async def get_user_applications_main_info_in_organization(
            self,
            user_id: int,
            activity_status: str | None = None,
    ) -> Sequence[ApplicationMainInfo]:

        stmt = (
            select(
                Application,
                Vacancy,
                Project,
            ).join(
                Vacancy, Vacancy.id == Application.vacancy_id,
            ).join(
                Project, Project.id == Vacancy.project_id,
            ).where(
                Application.user_id == user_id,
                Application.activity_status == activity_status,
            )
        )

        if activity_status is not None:
            stmt = stmt.where(Application.activity_status == activity_status)

        rows = await self.async_session.execute(
            stmt
        )
        tuples: Sequence[
            Row[
                Tuple[
                    Application,
                    Vacancy,
                    Project,
                ]
            ]
        ] = rows.all()

        result: Sequence[ApplicationMainInfo] = [
            ApplicationMainInfo(
                application_id=application.id,
                description=application.description,
                vacancy_id=vacancy.id,
                vacancy_name=vacancy.name,
                project_id=project.id,
                project_name=project.name,
                activity_status=ApplicationActivityStatusType(application.activity_status),
                created_at=application.created_at.isoformat(),
            ) for application, vacancy, project in tuples
        ]
        return result


    @log_calls
    async def get_active_application_by_user_and_vacancy(
            self,
            user_id: int,
            vacancy_id: int,
    ) -> Application | None:
        application = await self.async_session.execute(
            select(
                Application
            ).where(
                Application.user_id == user_id,
                Application.vacancy_id == vacancy_id,
                Application.activity_status == ApplicationActivityStatusType.ACTIVE.value,
            )
        )
        return application.scalar_one_or_none()

    @log_calls
    async def get_active_applications_by_user_and_project(
            self,
            user_id: int,
            project_id: int,
    ) -> Sequence[Application]:
        application = await self.async_session.execute(
            select(
                Application
            ).join(
                Vacancy, Vacancy.id == Application.vacancy_id,
            ).join(
                Project, Project.id == Vacancy.project_id,
            )
            .where(
                Application.user_id == user_id,
                Application.activity_status == ApplicationActivityStatusType.ACTIVE.value,
                Project.id == project_id,
            )
        )
        return application.scalars().all()

    @log_calls
    async def get_active_applications_by_user(
            self,
            user_id: int,
    ) -> Sequence[Application]:
        application = await self.async_session.execute(
            select(
                Application
            ).where(
                Application.user_id == user_id,
                Application.activity_status == ApplicationActivityStatusType.ACTIVE.value,
            )
        )
        return application.scalars().all()

    @log_calls
    async def get_active_applications_by_vacancy(
            self,
            vacancy_id: int,
    ) -> Sequence[Application]:
        application = await self.async_session.execute(
            select(
                Application
            ).where(
                Application.vacancy_id == vacancy_id,
                Application.activity_status == ApplicationActivityStatusType.ACTIVE.value,
            )
        )
        return application.scalars().all()

    @log_calls
    async def get_active_application_by_manager(
            self,
            user_id: int,
    ) -> Sequence[Application]:
        """
        Получить все активные отклики доступные для просмотра менеджеру
        """
        res = await self.async_session.execute(
            select(
                Application,
            ).join(
                Vacancy, Vacancy.id == Application.vacancy_id,
            ).join(
                Permission, Permission.resource_id == Vacancy.id,
            )
            .where(
                Application.user_id == user_id,
                Application.activity_status == ApplicationActivityStatusType.ACTIVE.value,
                Permission.resource_type == ResourceType.VACANCY,
                Permission.permission_type == PermissionType.EDIT_VACANCY,
            )
        )
        return res.scalars().all()


application_repo = get_repository(
    repo_type=ApplicationCRUDRepository
)

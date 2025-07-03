from typing import Sequence

from core.models import Project
from core.models.application import Application
from core.models.vacancy import Vacancy
from core.repository.crud.application import ApplicationCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.schemas.application import ApplicationShortInfo, ApplicationActivityStatusType
from core.services.interfaces.application import IApplicationService
from core.services.interfaces.permission import IPermissionService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists


class ApplicationService(IApplicationService):
    def __init__(
            self,
            project_repo: ProjectCRUDRepository,
            vacancy_repo: VacancyCRUDRepository,
            permission_service: IPermissionService,
            application_repo: ApplicationCRUDRepository,
    ):
        self.project_repo = project_repo
        self.vacancy_repo = vacancy_repo
        self.permission_service = permission_service
        self.application_repo = application_repo

    async def get_all_active_applications_by_user_and_project(
            self,
            user_id: int,
            project_id: int,
    ) -> Sequence[ApplicationShortInfo]:
        """
        Получить список всех активных откликов пользователя в проекте
        """
        project: Project | None = (
            await self.project_repo.get_project_by_id(
                project_id=project_id,
            )
        )
        if not project:
            raise EntityDoesNotExist('Указанный проект не существует')

        applications: Sequence[Application] = (
            await self.application_repo.get_active_applications_by_user_and_project(
                user_id=user_id,
                project_id=project.id,
            )
        )
        res = [
            ApplicationShortInfo(
                application_id=app.id,
                vacancy_id=app.vacancy_id,
            ) for app in applications
        ]
        return res

    async def create_application(
            self,
            user_id: int,
            vacancy_id: int,
            description: str,
    ) -> ...:
        """
        Создать отклик на вакансию
        """
        vacancy: Vacancy | None = (
            await self.vacancy_repo.get_vacancy_by_id(
                vacancy_id=vacancy_id,
            )
        )
        if not vacancy:
            raise EntityDoesNotExist('Вакансия не существует')

        application: Application | None = (
            await self.application_repo.get_active_application_by_user_and_vacancy(
                user_id=user_id,
                vacancy_id=vacancy_id,
            )
        )
        if application:
            raise EntityAlreadyExists('Активный отклик с этим пользователем и вакансией уже существует')

        application: Application = (
            await self.application_repo.create_application(
                user_id=user_id,
                vacancy_id=vacancy_id,
                description=description,
                activity_status=ApplicationActivityStatusType.ACTIVE.value,
            )
        )
        return application

    async def change_application_status(
            self,
            application_id: int,
            status: str,
    ) -> ...:
        """
        Поменять статус вакансии
        """
        ...

    async def cancel_application(
            self,
            application_id: int,
    ) -> ...:
        """
        Отменить отклик от лица пользователя
        """
        ...

    async def reject_application(
            self,
            application_id: int,
    ) -> ...:
        """
        Отменить отклик от лица менеджера
        """
        ...

    async def reject_all_application_in_vacancy(
            self,
            vacancy_id: int,
    ) -> ...:
        """
        Отменить все отклики в вакансии от лица менеджера
        """
        ...

    async def reject_all_application_in_vacancy_except(
            self,
            vacancy_id: int,
            application_id: int,
    ) -> ...:
        """
        Отменить все отклики в вакансии от лица менеджера кроме указанного
        """
        ...

    async def delete_application(
            self,
            application_id: int,
    ) -> ...:
        """
        Удалить отклик (насовсем)
        """
        ...

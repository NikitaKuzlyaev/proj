from typing import Sequence, Any

from core.models import Project, Organization
from core.models.application import Application
from core.models.vacancy import Vacancy
from core.repository.crud.application import ApplicationCRUDRepository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.schemas.application import ApplicationShortInfo, ApplicationActivityStatusType, ApplicationMainInfo, \
    ApplicationId, ApplicationLimits
from core.services.interfaces.application import IApplicationService
from core.services.interfaces.permission import IPermissionService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.domain import ActiveEntityLimit
from core.utilities.loggers.log_decorator import log_calls

"""
SETTINGS
Убрать потом и сделать по нормальному
"""
# =====================

MAX_ACTIVE_APPLICATION_FOR_USER_IN_ORGANIZATION = 5


# =====================

class ApplicationService(IApplicationService):
    def __init__(
            self,
            project_repo: ProjectCRUDRepository,
            vacancy_repo: VacancyCRUDRepository,
            permission_service: IPermissionService,
            application_repo: ApplicationCRUDRepository,
            org_repo: OrganizationCRUDRepository,
    ):
        self.project_repo = project_repo
        self.vacancy_repo = vacancy_repo
        self.permission_service = permission_service
        self.application_repo = application_repo
        self.org_repo = org_repo

    @log_calls
    async def get_user_application_limits_in_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> ApplicationLimits:
        number_of_current_active_applications: int = (
            await self.get_number_of_active_user_applications_in_organization(
                user_id=user_id,
                org_id=org_id,
            )
        )
        res = ApplicationLimits(
            application_number_current=number_of_current_active_applications,
            application_number_max=MAX_ACTIVE_APPLICATION_FOR_USER_IN_ORGANIZATION,
        )
        return res

    @log_calls
    async def get_number_of_active_user_applications_in_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> int:
        res: Sequence[ApplicationMainInfo] = (
            await self.get_user_applications_main_info_in_organization(
                user_id=user_id,
                org_id=org_id,
                activity_status=ApplicationActivityStatusType.ACTIVE.value,
            )
        )
        return len(res)

    @log_calls
    async def get_user_applications_main_info_in_organization(
            self,
            user_id: int,
            org_id: int,
            activity_status: str | None = None,
    ) -> Sequence[ApplicationMainInfo]:
        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist('Указанная организация не существует')

        res: Sequence[ApplicationMainInfo] = (
            await self.application_repo.get_user_applications_main_info_in_organization(
                user_id=user_id,
                activity_status=activity_status,
            )
        )
        return res

    @log_calls
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

    @log_calls
    async def create_application(
            self,
            user_id: int,
            vacancy_id: int,
            description: str,
    ) -> ApplicationId:
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

        org: Organization | None = (
            await self.org_repo.get_organization_by_vacancy_id(
                vacancy_id=vacancy_id,
            )
        )
        if not org:
            raise EntityDoesNotExist('Организация не существует')

        number_of_active_user_applications_in_organization: int = (
            await self.get_number_of_active_user_applications_in_organization(
                user_id=user_id,
                org_id=org.id,
            )
        )
        if number_of_active_user_applications_in_organization >= MAX_ACTIVE_APPLICATION_FOR_USER_IN_ORGANIZATION:
            raise ActiveEntityLimit('Пользователь уже имеет максимальное число откликов в этой организации')

        application: Application = (
            await self.application_repo.create_application(
                user_id=user_id,
                vacancy_id=vacancy_id,
                description=description,
                activity_status=ApplicationActivityStatusType.ACTIVE.value,
            )
        )
        res = ApplicationId(application_id=application.id)
        return res

    @log_calls
    async def change_application_status(
            self,
            application_id: int,
            status: str,
    ) -> ApplicationId:
        """
        Поменять статус вакансии
        """
        application: Application | None = (
            await self.application_repo.get_application_by_id(
                application_id=application_id,
            )
        )
        if not application:
            raise EntityDoesNotExist('Отклика не существует')

        patched_application: Application | None = (
            await self.application_repo.patch_application(
                application_id=application.id,
                description=application.description,
                activity_status=status,
            )
        )
        if not patched_application:
            raise EntityDoesNotExist('Отклика не существует')

        return ApplicationId(application_id=patched_application.id)

    @log_calls
    async def cancel_application(
            self,
            application_id: int,
    ) -> ApplicationId:
        res = await self.change_application_status(
            application_id=application_id,
            status=ApplicationActivityStatusType.CANCELED.value,
        )
        return res

    @log_calls
    async def reject_application(
            self,
            application_id: int,
    ) -> ...:
        """
        Отменить отклик от лица менеджера
        """
        ...

    @log_calls
    async def reject_all_application_in_vacancy(
            self,
            vacancy_id: int,
    ) -> ...:
        """
        Отменить все отклики в вакансии от лица менеджера
        """
        ...

    @log_calls
    async def reject_all_application_in_vacancy_except(
            self,
            vacancy_id: int,
            application_id: int,
    ) -> ...:
        """
        Отменить все отклики в вакансии от лица менеджера кроме указанного
        """
        ...

    @log_calls
    async def delete_application(
            self,
            application_id: int,
    ) -> ...:
        """
        Удалить отклик (насовсем)
        """
        ...

from typing import Sequence, Protocol

from core.schemas.application import ApplicationShortInfo, ApplicationMainInfo, ApplicationId, ApplicationLimits


class IApplicationService(Protocol):


    async def create_application(
            self,
            user_id: int,
            vacancy_id: int,
            description: str,
    ) -> ApplicationId:
        """
        Создать отклик на вакансию
        """
        ...
    async def get_user_application_limits_in_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> ApplicationLimits:
        ...


    async def get_number_of_active_user_applications_in_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> int:
        ...

    async def get_user_applications_main_info_in_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> Sequence[ApplicationMainInfo]:
        ...

    async def get_all_active_applications_by_user_and_project(
            self,
            user_id: int,
            project_id: int,
    ) -> Sequence[ApplicationShortInfo]:
        """
        Получить список всех активных откликов пользователя в проекте
        """
        ...

    async def change_application_status(
            self,
            application_id: int,
            status: str,
    ) -> ApplicationId:
        """
        Поменять статус вакансии
        """
        ...

    async def cancel_application(
            self,
            application_id: int,
    ) -> ApplicationId:
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

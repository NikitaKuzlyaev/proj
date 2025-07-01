from typing import Sequence, Protocol

from core.models.vacancy import Vacancy
from core.schemas.project import ProjectVacanciesShortInfoResponse
from core.schemas.vacancy import VacancyShortInfoResponse, VacancyCreateResponse, VacancyPatchResponse


class IVacancyService(Protocol):


    async def get_all_vacancies_in_project(
            self,
            project_id: int,
    ) -> Sequence[Vacancy]:
        ...

    async def get_all_vacancies_in_project_detailed_info(
            self,
            project_id: int,
            user_id: int
    ) -> Sequence[ProjectVacanciesShortInfoResponse]:
        ...

    async def get_vacancy_by_id(
            self,
            vacancy_id: int,
    ) -> Vacancy:
        ...

    async def get_vacancy_short_info_response(
            self,
            vacancy_id: int,
            user_id: int,
    ) -> VacancyShortInfoResponse:
        ...

    async def create_vacancy(
            self,
            user_id: int,
            project_id: int,
            name: str,
            short_description: str,
            activity_status: str,
            visibility: str,
    ) -> VacancyCreateResponse:
        ...

    async def patch_vacancy(
            self,
            user_id: int,
            vacancy_id: int,
            project_id: int,
            name: str,
            short_description: str,
            visibility: str,
            activity_status: str,
    ) -> VacancyPatchResponse:
        ...

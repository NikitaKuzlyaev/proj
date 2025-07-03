from typing import Sequence

from core.models import Vacancy
from core.schemas.application import ApplicationShortInfo
from core.schemas.project import ProjectVacanciesFullInfoResponse
from core.schemas.vacancy import VacancyShortInfoResponse, VacancyActivityStatusType, VacancyVisibilityType, \
    VacancyCreateResponse, VacancyPatchResponse
from core.utilities.loggers.log_decorator import log_calls


class VacancyMapper:
    def __init__(
            self,
    ):
        return

    @log_calls
    def update_vacancies_full_info_response_by_active_applications(
            self,
            base: Sequence[ProjectVacanciesFullInfoResponse],
            active_applications: Sequence[ApplicationShortInfo],
    ) -> Sequence[ProjectVacanciesFullInfoResponse]:
        ids = set(app.vacancy_id for app in active_applications)

        for app in base:
            if app.can_user_edit:
                continue
            if app.vacancy_id in ids:
                app.has_user_active_applications = True
                app.can_user_make_applications = False


        return base

    @log_calls
    def vacancy_to_short_info_response(
            self,
            vacancy: Vacancy,
    ) -> VacancyShortInfoResponse:
        res = VacancyShortInfoResponse(
            vacancy_id=vacancy.id,
            project_id=vacancy.project_id,
            name=vacancy.name,
            short_description=vacancy.short_description,
            activity_status=VacancyActivityStatusType(vacancy.activity_status),
            visibility=VacancyVisibilityType(vacancy.visibility),
        )
        return res

    @log_calls
    def vacancy_to_create_response(
            self,
            vacancy: Vacancy,
    ) -> VacancyCreateResponse:
        res = VacancyCreateResponse(
            vacancy_id=vacancy.id,
        )
        return res

    @log_calls
    def vacancy_to_patch_response(
            self,
            vacancy: Vacancy,
    ) -> VacancyPatchResponse:
        res = VacancyPatchResponse(
            vacancy_id=vacancy.id,
        )
        return res


def get_vacancy_mapper(
) -> VacancyMapper:
    return VacancyMapper()

from typing import Sequence, Tuple

from sqlalchemy import select, update, Row, and_

from core.dependencies.repository import get_repository
from core.models import Project
from core.models.permissions import Permission, PermissionType, ResourceType
from core.models.user import User
from core.models.vacancy import Vacancy
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.project import ProjectManagerInfo, ProjectOfVacancyInfo, ProjectVacanciesShortInfoResponse
from core.schemas.vacancy import VacancyActivityStatusType, VacancyVisibilityType
from core.utilities.loggers.log_decorator import log_calls


class VacancyCRUDRepository(BaseCRUDRepository):
    @log_calls
    async def get_all_vacancies_in_project(
            self,
            project_id: int,
    ) -> Sequence[Vacancy] | None:
        """
        Получить все объекты Vacancy c Vacancy.project_id == project_id
        :param project_id: id объекта Project
        :return: последовательность объектов Vacancy или None
        """
        result = await self.async_session.execute(
            select(
                Vacancy
            ).where(
                Vacancy.project_id == project_id,
            )
        )
        vacancies = result.scalars().all()
        return vacancies

    @log_calls
    async def get_all_vacancies_in_project_detailed_info(
            self,
            project_id: int,
            user_id: int,
    ) -> Sequence[ProjectVacanciesShortInfoResponse]:
        stmt = (
            select(
                Vacancy,
                Project,
                User,
                Permission.id.label("permission_id_for_edit_vacancy"),
            )
            .join(
                Project,
                Project.id == Vacancy.project_id,
            )
            .join(User,
                  User.id == Vacancy.creator_id,
                  )
            .outerjoin(
                Permission,
                and_(
                    Permission.user_id == user_id,
                    Permission.resource_type == ResourceType.VACANCY.value,
                    Permission.resource_id == Vacancy.id,
                    Permission.permission_type == PermissionType.EDIT_VACANCY.value,
                )
            )
            .where(
                Project.id == project_id,
            )
        )

        rows = await self.async_session.execute(stmt)
        tuples: Sequence[
            Row[
                Tuple[
                    Vacancy,
                    Project,
                    User,
                    int | None
                ]
            ]
        ] = rows.all()

        result: Sequence[ProjectVacanciesShortInfoResponse] = \
            [
                ProjectVacanciesShortInfoResponse(
                    vacancy_id=vacancy.id,
                    manager=ProjectManagerInfo(
                        user_id=manager.id,
                        avatar='',
                        name=manager.username,
                    ),
                    project=ProjectOfVacancyInfo(
                        id=project.id,
                        name=project.name,
                    ),
                    name=vacancy.name,
                    short_description=vacancy.short_description,
                    number_of_offers=0,
                    number_of_responses=0,
                    created_at=vacancy.created_at.isoformat(),
                    activity_status=VacancyActivityStatusType(vacancy.activity_status),
                    visibility=VacancyVisibilityType(vacancy.visibility),
                    can_user_edit=(
                        not permission_for_edit_vacancy is None
                    ),
                    can_user_make_response=(
                            vacancy.activity_status == VacancyActivityStatusType.ACTIVE and
                            vacancy.visibility == VacancyVisibilityType.OPEN
                    ),
                ) for vacancy, project, manager, permission_for_edit_vacancy in tuples
            ]

        return result

    @log_calls
    async def get_vacancy_by_id(
            self,
            vacancy_id: int,
    ) -> Vacancy | None:
        """
        Получить объект Vacancy с указанным id
        :param vacancy_id: id объекта Vacancy
        :return: объект Vacancy или None
        """
        result = await self.async_session.execute(
            select(
                Vacancy
            ).where(
                Vacancy.id == vacancy_id
            )
        )
        vacancy = result.scalars().one_or_none()
        return vacancy

    @log_calls
    async def patch_vacancy_by_id(
            self,
            vacancy_id: int,
            project_id: int,
            name: str,
            short_description: str,
            visibility: str,
            activity_status: str
    ) -> Vacancy | None:
        stmt = (
            update(Vacancy)
            .where(Vacancy.id == vacancy_id)
            .values(
                project_id=project_id,
                name=name,
                short_description=short_description,
                visibility=visibility,
                activity_status=activity_status
            )
            .execution_options(synchronize_session="fetch")
        )

        await self.async_session.execute(stmt)
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(Vacancy).where(Vacancy.id == vacancy_id)
        )
        return result.scalar_one_or_none()

    @log_calls
    async def create_vacancy(
            self,
            project_id: int,
            user_id: int,
            name: str,
            short_description: str,
            activity_status: str,
            visibility: str,
    ) -> Vacancy:
        new_vacancy = Vacancy(
            name=name,
            creator_id=user_id,
            project_id=project_id,
            short_description=short_description,
            activity_status=activity_status,
            visibility=visibility
        )

        self.async_session.add(instance=new_vacancy)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_vacancy)

        return new_vacancy


vacancy_repo = get_repository(repo_type=VacancyCRUDRepository)

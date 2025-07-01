from typing import Sequence

from fastapi import HTTPException

from core.models import Project
from core.models.vacancy import Vacancy
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.schemas.permission import PermissionsShortResponse
from core.schemas.project import ProjectVacanciesShortInfoResponse
from core.schemas.vacancy import VacancyShortInfoResponse, VacancyCreateResponse, VacancyPatchResponse
from core.services.interfaces.permission import IPermissionService
from core.services.mappers.vacancy import VacancyMapper


class VacancyService:
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            project_repo: ProjectCRUDRepository,
            vacancy_repo: VacancyCRUDRepository,
            vacancy_mapper: VacancyMapper,
            permission_service: IPermissionService,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.project_repo = project_repo
        self.vacancy_repo = vacancy_repo
        self.vacancy_mapper = vacancy_mapper
        self.permission_service = permission_service

    async def get_all_vacancies_in_project(
            self,
            project_id: int,
    ) -> Sequence[Vacancy]:
        res: Sequence[Vacancy] = (
            await self.vacancy_repo.get_all_vacancies_in_project(
                project_id=project_id,
            )
        )
        return res

    async def get_all_vacancies_in_project_detailed_info(
            self,
            project_id: int,
            user_id: int
    ) -> Sequence[ProjectVacanciesShortInfoResponse]:
        project: Project = (
            await self.project_repo.get_project_by_id(
                project_id=project_id,
            )
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        res: Sequence[ProjectVacanciesShortInfoResponse] = (
            await self.vacancy_repo.get_all_vacancies_in_project_detailed_info(
                project_id=project.id,
                user_id=user_id,
            )
        )
        return res

    async def get_vacancy_by_id(
            self,
            vacancy_id: int,
    ) -> Vacancy:
        res: Vacancy = (
            await self.vacancy_repo.get_vacancy_by_id(
                vacancy_id=vacancy_id,
            )
        )
        return res

    async def get_vacancy_short_info_response(
            self,
            vacancy_id: int,
            user_id: int,
    ) -> VacancyShortInfoResponse:
        vacancy: Vacancy = (
            await self.vacancy_repo.get_vacancy_by_id(
                vacancy_id=vacancy_id,
            )
        )
        res: VacancyShortInfoResponse = (
            self.vacancy_mapper.vacancy_to_short_info_response(
                vacancy=vacancy,
            )
        )
        return res

    async def create_vacancy(
            self,
            user_id: int,
            project_id: int,
            name: str,
            short_description: str,
            activity_status: str,
            visibility: str,
    ) -> VacancyCreateResponse:
        project: Project = (
            await self.project_repo.get_project_by_id(
                project_id=project_id,
            )
        )
        if not project:
            raise Exception("Project not found")

        vacancy: Vacancy = (
            await self.vacancy_repo.create_vacancy(
                project_id=project_id,
                user_id=user_id,
                name=name,
                short_description=short_description,
                activity_status=activity_status,
                visibility=visibility,
            )
        )
        permission: PermissionsShortResponse = (
            await self.permission_service.allow_user_edit_vacancy(
                user_id=user_id,
                vacancy_id=vacancy.id,
            )
        )
        res: VacancyCreateResponse = (
            self.vacancy_mapper.vacancy_to_create_response(
                vacancy=vacancy,
            )
        )
        return res

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
        if not all([
            await self.permission_service.can_user_edit_vacancy(
                user_id=user_id,
                vacancy_id=vacancy_id,
            ),

        ]):
            raise HTTPException(status_code=403, detail="Permission denied")

        project: Project = (
            await self.project_repo.get_project_by_id(
                project_id=project_id,
            )
        )
        if not project:
            raise Exception("Project not found")

        try:
            vacancy: Vacancy = (
                await self.vacancy_repo.patch_vacancy_by_id(
                    vacancy_id=vacancy_id,
                    project_id=project_id,
                    name=name,
                    short_description=short_description,
                    visibility=visibility,
                    activity_status=activity_status,
                )
            )
            if not vacancy is Vacancy:
                raise HTTPException(status_code=400, detail="???")

            res: VacancyPatchResponse = (
                self.vacancy_mapper.vacancy_to_patch_response(
                    vacancy=vacancy,
                )
            )
            return res
        except Exception as e:
            raise e



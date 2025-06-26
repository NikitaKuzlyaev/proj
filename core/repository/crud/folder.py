import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.dependencies.repository import get_repository
#from core.models import Folder
#from core.schemas.folder import FolderInCreate, RootFolderInCreate

#from core.schemas.user import UserInCreate, UserInLogin, UserInUpdate
from core.models.user import User

from core.schemas.organization import OrganizationInCreate
from core.models.organization import Organization

from core.repository.crud.base import BaseCRUDRepository
from core.services.securities.hashing import pwd_generator
from core.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from core.utilities.exceptions.auth import PasswordDoesNotMatch
from core.services.securities.credential import account_credential_verifier


# class FolderCRUDRepository(BaseCRUDRepository):
#
#     async def create_root_folder(
#             self,
#             root_folder_create: RootFolderInCreate
#     ) -> Folder:
#
#         new_folder = Folder(name=root_folder_create.name,
#                                   creator_id=root_folder_create.creator_id
#                                   )
#
#         self.async_session.add(instance=new_folder)
#         await self.async_session.commit()
#         await self.async_session.refresh(instance=new_folder)
#
#         return new_folder
#
#
# folder_repo = get_repository(repo_type=FolderCRUDRepository)

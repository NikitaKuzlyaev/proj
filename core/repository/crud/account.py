import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.dependencies.repository import get_repository
from core.schemas.account import AccountInCreate, AccountInLogin, AccountInUpdate
from core.models.account import Account
from core.repository.crud.base import BaseCRUDRepository
from core.services.securities.hashing import pwd_generator
from core.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from core.utilities.exceptions.auth import PasswordDoesNotMatch
from core.services.securities.credential import account_credential_verifier


class AccountCRUDRepository(BaseCRUDRepository):
    async def create_account(self, account_create: AccountInCreate) -> Account:
        new_account = Account(username=account_create.username)

        new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        new_account.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=new_account.hash_salt, new_password=account_create.password
            )
        )

        self.async_session.add(instance=new_account)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_account)

        return new_account

    async def read_accounts(self) -> typing.Sequence[Account]:
        stmt = sqlalchemy.select(Account)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_account_by_id(self, id_: int) -> Account:
        stmt = sqlalchemy.select(Account).where(Account.id == id_)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with id `{id}` does not exist!")

        return query.scalar()

    async def read_account_by_username(self, username: str) -> Account:
        stmt = sqlalchemy.select(Account).where(Account.username == username)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with username `{username}` does not exist!")

        return query.scalar()

    async def read_user_by_password_authentication(self, account_login: AccountInLogin) -> Account:
        stmt = sqlalchemy.select(Account).where(
            Account.username == account_login.username,
        )
        query = await self.async_session.execute(statement=stmt)
        db_account = query.scalar()

        if not db_account:
            raise EntityDoesNotExist("Wrong username or wrong email!")

        if not pwd_generator.is_password_authenticated(hash_salt=db_account.hash_salt, password=account_login.password,
                                                       hashed_password=db_account.hashed_password):
            raise PasswordDoesNotMatch("Password does not match!")

        return db_account

    async def delete_account_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(Account).where(Account.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_account = query.scalar()

        if not delete_account:
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")

        stmt = sqlalchemy.delete(table=Account).where(Account.id == delete_account.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Account with id '{id}' is successfully deleted!"

    async def is_username_taken(self, username: str) -> bool:
        username_stmt = sqlalchemy.select(Account.username).select_from(Account).where(Account.username == username)
        username_query = await self.async_session.execute(username_stmt)
        db_username = username_query.scalar()

        if not account_credential_verifier.is_username_available(username=db_username):
            raise EntityAlreadyExists(f"The username `{username}` is already taken!")

        return True

account_repo = get_repository(repo_type=AccountCRUDRepository)
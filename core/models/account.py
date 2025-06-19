from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy import text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions
from core.database.connection import Base


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    username: Mapped[str] = mapped_column(
        String(length=64), nullable=False, unique=True
    )
    _hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    _hash_salt: Mapped[str] = mapped_column(String(length=1024), nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )

    __mapper_args__ = {"eager_defaults": True}

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    def set_hashed_password(self, hashed_password: str) -> None:
        self._hashed_password = hashed_password

    @property
    def hash_salt(self) -> str:
        return self._hash_salt

    def set_hash_salt(self, hash_salt: str) -> None:
        self._hash_salt = hash_salt

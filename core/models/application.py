import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base
from core.schemas.application import ApplicationActivityStatusType


class Application(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement="auto"
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id"),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(length=512),
        nullable=True
    )

    activity_status = Column(
        String,
        nullable=False,
        default=ApplicationActivityStatusType.INACTIVE.value
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )

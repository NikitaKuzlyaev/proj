import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base
from core.models.user import User
from core.schemas.organization import OrganizationJoinPolicyType, OrganizationActivityStatusType, \
    OrganizationVisibilityType


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement="auto"
    )

    name: Mapped[str] = mapped_column(
        String(length=64),
        nullable=False,
        unique=False
    )

    short_description: Mapped[str] = mapped_column(
        String(length=512),
        nullable=True
    )

    long_description: Mapped[str] = mapped_column(
        String(length=4096),
        nullable=True
    )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )

    join_policy = Column(
        String,
        nullable=False,
        default=OrganizationJoinPolicyType.CLOSED.value
    )

    activity_status = Column(
        String,
        nullable=False,
        default=OrganizationActivityStatusType.INACTIVE.value
    )

    visibility = Column(
        String,
        nullable=False,
        default=OrganizationVisibilityType.CLOSED.value
    )
    # ------------------------------------------------------------------------------------------------------------------
    # Для удобной работы со связями
    creator: Mapped["User"] = relationship("User")

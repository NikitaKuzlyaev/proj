import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


class OrganizationMember(Base):
    __tablename__ = "organization_member"

    # для связки user--organization
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement="auto"
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"),
        nullable=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'organization_id', name='_user_org_uc'),
    )

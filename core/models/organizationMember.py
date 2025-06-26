from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy import text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions
from core.database.connection import Base
#from core.models.folder import Folder
from core.models.user import User


class OrganizationMember(Base):
    __tablename__ = "organization_member"

    # для связки user--organization
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'organization_id', name='_user_org_uc'),
    )

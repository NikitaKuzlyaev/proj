from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
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
from core.models.organization import Organization
from core.schemas.project import ProjectActivityStatusType, ProjectVisibilityType


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(
        String(length=64), nullable=False, unique=True
    )

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)

    short_description: Mapped[str] = mapped_column(String(length=512), nullable=True)
    long_description: Mapped[str] = mapped_column(String(length=4096), nullable=True)

    activity_status = Column(String, nullable=False, default=ProjectActivityStatusType.INACTIVE.value)
    visibility = Column(String, nullable=False, default=ProjectVisibilityType.CLOSED.value)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )

    # ------------------------------------------------------------------------------------------------------------------
    # Для удобной работы со связями
    creator: Mapped["User"] = relationship("User")

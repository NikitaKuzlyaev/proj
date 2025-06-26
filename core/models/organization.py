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
from core.schemas.organization import OrganizationJoinPolicy


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(
        String(length=64), nullable=False, unique=False
    )

    short_description: Mapped[str] = mapped_column(String(length=512), nullable=True)
    long_description: Mapped[str] = mapped_column(String(length=4096), nullable=True)

    #root_folder_id: Mapped[int] = mapped_column(ForeignKey("folder.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )

    join_policy = Column(String, nullable=False, default=OrganizationJoinPolicy.CLOSED.value)
    # ------------------------------------------------------------------------------------------------------------------
    # Для удобной работы со связями
    #root_folder: Mapped["Folder"] = relationship("Folder")
    creator: Mapped["User"] = relationship("User")

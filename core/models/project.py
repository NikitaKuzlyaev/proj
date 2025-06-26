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


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(
        String(length=64), nullable=False, unique=True
    )
    #root_folder_id: Mapped[int] = mapped_column(ForeignKey("folder.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )

    # ------------------------------------------------------------------------------------------------------------------
    # Для удобной работы со связями
    #root_folder: Mapped["Folder"] = relationship("Folder")
    creator: Mapped["User"] = relationship("User")

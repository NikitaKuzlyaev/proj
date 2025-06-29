import enum

from sqlalchemy import Enum
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from core.database.connection import Base


class PermissionType(enum.Enum):
    EDIT_ORGANIZATION = "EDIT_ORGANIZATION"
    CREATE_ORGANIZATION = "CREATE_ORGANIZATION"
    CREATE_PROJECTS_INSIDE_ORGANIZATION = "CREATE_PROJECTS_INSIDE_ORGANIZATION"
    EDIT_VACANCY = "EDIT_VACANCY"


class ResourceType(enum.Enum):
    ORGANIZATION = "ORGANIZATION"
    PROJECT = "PROJECT"
    VACANCY = "VACANCY"


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    resource_type: Mapped[ResourceType] = mapped_column(
        Enum(ResourceType)
    )

    resource_id: Mapped[int] = mapped_column(
        nullable=True
    )

    permission_type: Mapped[PermissionType] = mapped_column(
        Enum(PermissionType)
    )

    __table_args__ = (
        Index("ix_permission_scope", "user_id", "resource_type", "resource_id"),
    )

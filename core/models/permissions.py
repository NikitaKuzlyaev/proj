import enum

from sqlalchemy import Enum
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from core.database.connection import Base


class PermissionType(enum.Enum):
    # --- [ORGANIZATION] ---
    EDIT_ORGANIZATION = "EDIT_ORGANIZATION"
    DELETE_ORGANIZATION_MEMBERS = "DELETE_ORGANIZATION_MEMBERS"

    # --- [PROJECT] ---
    CREATE_PROJECTS_INSIDE_ORGANIZATION = "CREATE_PROJECTS_INSIDE_ORGANIZATION"
    EDIT_PROJECT = "EDIT_PROJECT"

    # --- [VACANCY] ---
    EDIT_VACANCY = "EDIT_VACANCY"

    # --- [DOMAIN] ---
    ADMIN = "ADMIN"
    CREATE_ORGANIZATION = "CREATE_ORGANIZATION"

class ResourceType(enum.Enum):
    ORGANIZATION = "ORGANIZATION"
    PROJECT = "PROJECT"
    VACANCY = "VACANCY"
    DOMAIN = "DOMAIN"


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(
        primary_key=True,
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

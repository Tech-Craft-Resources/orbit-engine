import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from pydantic import EmailStr, field_validator
from sqlalchemy import Column, DateTime, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from collections.abc import Sequence


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# ============================================================================
# ORGANIZATION MODELS
# ============================================================================


class OrganizationBase(SQLModel):
    name: str = Field(max_length=255)
    slug: str = Field(max_length=100, index=True)
    description: str | None = Field(default=None)
    logo_url: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Validate slug format: lowercase, alphanumeric and hyphens only"""
        import re

        if not re.match(r"^[a-z0-9-]{3,50}$", v):
            raise ValueError(
                "Slug must be 3-50 characters, lowercase letters, numbers and hyphens only"
            )
        return v


class Organization(OrganizationBase, table=True):
    __tablename__ = "organizations"
    __table_args__ = (
        Index("idx_organizations_slug", "slug", unique=True),
        Index("idx_organizations_is_active", "is_active"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    users: list["User"] = Relationship(back_populates="organization")


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    logo_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


class OrganizationPublic(OrganizationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ============================================================================
# ROLE MODELS
# ============================================================================


class RoleBase(SQLModel):
    name: str = Field(max_length=50, index=True)
    description: str | None = None
    permissions: list[str] = Field(default_factory=list, sa_column=Column(JSONB))  # type: ignore


class Role(RoleBase, table=True):
    __tablename__ = "roles"
    __table_args__ = (Index("idx_roles_name", "name", unique=True),)

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    users: list["User"] = Relationship(back_populates="role")


class RolePublic(RoleBase):
    id: int
    created_at: datetime


class RolesPublic(SQLModel):
    data: list[RolePublic]
    count: int


# ============================================================================
# USER MODELS
# ============================================================================


class UserBase(SQLModel):
    email: EmailStr = Field(max_length=255, index=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    avatar_url: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)


class User(UserBase, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "email",
            name="uq_users_organization_email",
        ),
        Index("idx_users_organization_id", "organization_id"),
        Index("idx_users_role_id", "role_id"),
        Index("idx_users_is_active", "is_active"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", index=True)
    role_id: int = Field(foreign_key="roles.id", index=True)
    hashed_password: str = Field(max_length=255)
    last_login_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    failed_login_attempts: int = Field(default=0)
    locked_until: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    organization: Organization = Relationship(back_populates="users")
    role: Role = Relationship(back_populates="users")


class UserCreate(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    role_id: int


class UserRegister(SQLModel):
    """Schema for user registration during organization signup"""

    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=50)


class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    avatar_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None
    role_id: int | None = None


class UserUpdateMe(SQLModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class UserPublic(UserBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    role_id: int
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class UserPublicWithRelations(UserPublic):
    """User with organization and role included"""

    organization: OrganizationPublic
    role: RolePublic


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# ============================================================================
# ORGANIZATION SIGNUP
# ============================================================================


class OrganizationSignup(SQLModel):
    """Schema for creating a new organization with admin user"""

    # Organization data
    organization_name: str = Field(max_length=255)
    organization_slug: str = Field(max_length=100)
    organization_description: str | None = None

    # Admin user data
    admin_email: EmailStr = Field(max_length=255)
    admin_password: str = Field(min_length=8, max_length=128)
    admin_first_name: str = Field(max_length=100)
    admin_last_name: str = Field(max_length=100)
    admin_phone: str | None = Field(default=None, max_length=50)

    @field_validator("organization_slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Validate slug format"""
        import re

        if not re.match(r"^[a-z0-9-]{3,50}$", v):
            raise ValueError(
                "Slug must be 3-50 characters, lowercase letters, numbers and hyphens only"
            )
        return v


# ============================================================================
# AUTHENTICATION MODELS
# ============================================================================


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str  # User ID
    organization_id: str  # Organization ID
    role: str  # Role name


class LoginResponse(Token):
    """Response after successful login with user data"""

    user: UserPublicWithRelations


# ============================================================================
# GENERIC MODELS
# ============================================================================


class Message(SQLModel):
    message: str


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)

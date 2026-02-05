from typing import Any
import uuid

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    User,
    UserCreate,
    UserUpdate,
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
    Role,
)


# ============================================================================
# ORGANIZATION CRUD
# ============================================================================


def create_organization(
    *, session: Session, organization_create: OrganizationCreate
) -> Organization:
    """Create a new organization"""
    db_obj = Organization.model_validate(organization_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_organization_by_id(
    *, session: Session, organization_id: uuid.UUID
) -> Organization | None:
    """Get organization by ID"""
    return session.get(Organization, organization_id)


def get_organization_by_slug(*, session: Session, slug: str) -> Organization | None:
    """Get organization by slug"""
    statement = select(Organization).where(Organization.slug == slug)
    return session.exec(statement).first()


def update_organization(
    *,
    session: Session,
    db_organization: Organization,
    organization_in: OrganizationUpdate,
) -> Organization:
    """Update an organization"""
    organization_data = organization_in.model_dump(exclude_unset=True)
    db_organization.sqlmodel_update(organization_data)
    session.add(db_organization)
    session.commit()
    session.refresh(db_organization)
    return db_organization


# ============================================================================
# ROLE CRUD
# ============================================================================


def get_role_by_id(*, session: Session, role_id: int) -> Role | None:
    """Get role by ID"""
    return session.get(Role, role_id)


def get_role_by_name(*, session: Session, name: str) -> Role | None:
    """Get role by name"""
    statement = select(Role).where(Role.name == name)
    return session.exec(statement).first()


def get_roles(*, session: Session) -> list[Role]:
    """Get all roles"""
    statement = select(Role)
    return list(session.exec(statement).all())


# ============================================================================
# USER CRUD
# ============================================================================


def create_user(
    *, session: Session, user_create: UserCreate, organization_id: uuid.UUID
) -> User:
    """Create a new user within an organization"""
    db_obj = User.model_validate(
        user_create,
        update={
            "hashed_password": get_password_hash(user_create.password),
            "organization_id": organization_id,
        },
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    """Update a user"""
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
        del user_data["password"]
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(
    *, session: Session, email: str, organization_id: uuid.UUID | None = None
) -> User | None:
    """
    Get user by email.
    If organization_id is provided, search within that organization only.
    """
    statement = select(User).where(User.email == email).where(User.deleted_at.is_(None))
    if organization_id:
        statement = statement.where(User.organization_id == organization_id)
    return session.exec(statement).first()


def get_user_by_id(
    *, session: Session, user_id: uuid.UUID, organization_id: uuid.UUID | None = None
) -> User | None:
    """
    Get user by ID.
    If organization_id is provided, ensure the user belongs to that organization.
    """
    statement = select(User).where(User.id == user_id).where(User.deleted_at.is_(None))
    if organization_id:
        statement = statement.where(User.organization_id == organization_id)
    return session.exec(statement).first()


def get_users_by_organization(
    *, session: Session, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[User]:
    """Get all users for an organization"""
    statement = (
        select(User)
        .where(User.organization_id == organization_id)
        .where(User.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_users_by_organization(*, session: Session, organization_id: uuid.UUID) -> int:
    """Count users in an organization"""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(User)
        .where(User.organization_id == organization_id)
        .where(User.deleted_at.is_(None))
    )
    return session.exec(statement).one()


# ============================================================================
# AUTHENTICATION
# ============================================================================

# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(
    *,
    session: Session,
    email: str,
    password: str,
    organization_id: uuid.UUID | None = None,
) -> User | None:
    """
    Authenticate a user by email and password.
    If organization_id is provided, search within that organization only.
    """
    db_user = get_user_by_email(
        session=session, email=email, organization_id=organization_id
    )
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user

import uuid
from typing import Any
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app import crud
from app.api.deps import (
    CurrentUser,
    CurrentAdminUser,
    CurrentOrganization,
    SessionDep,
    require_role,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    Message,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.utils import generate_new_account_email, send_email

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersPublic)
def read_users(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users in current organization.

    Only admin users can list all users.
    """
    # Check if user is admin
    role = session.get(crud.Role, current_user.role_id)
    if not role or role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can list users",
        )

    users = crud.get_users_by_organization(
        session=session, organization_id=current_organization, skip=skip, limit=limit
    )
    count = crud.count_users_by_organization(
        session=session, organization_id=current_organization
    )

    return UsersPublic(data=users, count=count)


@router.post("/", response_model=UserPublic)
def create_user(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    user_in: UserCreate,
) -> Any:
    """
    Create new user in current organization.

    Only admin users can create users.
    """
    # Check if user is admin
    role = session.get(crud.Role, current_user.role_id)
    if not role or role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can create users",
        )

    # Check if email already exists in this organization
    existing_user = crud.get_user_by_email(
        session=session, email=user_in.email, organization_id=current_organization
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists in your organization",
        )

    # Validate role_id
    requested_role = session.get(crud.Role, user_in.role_id)
    if not requested_role:
        raise HTTPException(
            status_code=400,
            detail="Invalid role_id",
        )

    user = crud.create_user(
        session=session, user_create=user_in, organization_id=current_organization
    )

    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """
    Update own user.
    """
    if user_in.email:
        existing_user = crud.get_user_by_email(
            session=session,
            email=user_in.email,
            organization_id=current_user.organization_id,
        )
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    current_user.updated_at = datetime.now(timezone.utc)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    verified, _ = verify_password(body.current_password, current_user.hashed_password)
    if not verified:
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    current_user.updated_at = datetime.now(timezone.utc)
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")


@router.delete("/me", response_model=Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user (soft delete).
    """
    # Check if user is the only admin
    role = session.get(crud.Role, current_user.role_id)
    if role and role.name == "admin":
        # Count other active admins in the organization
        from sqlalchemy import func

        admin_count = session.exec(
            select(func.count())
            .select_from(User)
            .where(User.organization_id == current_user.organization_id)
            .where(User.role_id == role.id)
            .where(User.is_active == True)
            .where(User.deleted_at.is_(None))
            .where(User.id != current_user.id)
        ).one()

        if admin_count == 0:
            raise HTTPException(
                status_code=403,
                detail="Cannot delete the only admin user in the organization",
            )

    # Soft delete
    current_user.deleted_at = datetime.now(timezone.utc)
    current_user.is_active = False
    session.add(current_user)
    session.commit()
    return Message(message="User deleted successfully")


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Get a specific user by id in the current organization.
    """
    user = crud.get_user_by_id(
        session=session, user_id=user_id, organization_id=current_organization
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Users can only see themselves unless they're admin
    if user.id != current_user.id:
        role = session.get(crud.Role, current_user.role_id)
        if not role or role.name != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only administrators can view other users",
            )

    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.

    Only admin users can update other users.
    """
    # Check if current user is admin
    role = session.get(crud.Role, current_user.role_id)
    if not role or role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can update users",
        )

    db_user = crud.get_user_by_id(
        session=session, user_id=user_id, organization_id=current_organization
    )
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found in your organization",
        )

    if user_in.email:
        existing_user = crud.get_user_by_email(
            session=session,
            email=user_in.email,
            organization_id=current_organization,
        )
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    # Validate role_id if provided
    if user_in.role_id:
        requested_role = session.get(crud.Role, user_in.role_id)
        if not requested_role:
            raise HTTPException(
                status_code=400,
                detail="Invalid role_id",
            )

    db_user = crud.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete("/{user_id}", response_model=Message)
def delete_user(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    user_id: uuid.UUID,
) -> Message:
    """
    Delete a user (soft delete).

    Only admin users can delete users.
    """
    # Check if current user is admin
    role = session.get(crud.Role, current_user.role_id)
    if not role or role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can delete users",
        )

    user = crud.get_user_by_id(
        session=session, user_id=user_id, organization_id=current_organization
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete yourself. Use DELETE /users/me instead",
        )

    # Check if this is the only admin
    user_role = session.get(crud.Role, user.role_id)
    if user_role and user_role.name == "admin":
        from sqlalchemy import func

        admin_count = session.exec(
            select(func.count())
            .select_from(User)
            .where(User.organization_id == current_organization)
            .where(User.role_id == user_role.id)
            .where(User.is_active == True)
            .where(User.deleted_at.is_(None))
        ).one()

        if admin_count <= 1:
            raise HTTPException(
                status_code=403,
                detail="Cannot delete the only admin user in the organization",
            )

    # Soft delete
    user.deleted_at = datetime.now(timezone.utc)
    user.is_active = False
    session.add(user)
    session.commit()
    return Message(message="User deleted successfully")

from collections.abc import Generator
from typing import Annotated
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import TokenPayload, User, Organization, Role

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """Get current authenticated user from JWT token"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    # Get user with relationships
    user = session.exec(
        select(User)
        .where(User.id == uuid.UUID(token_data.sub))
        .where(User.deleted_at.is_(None))
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_organization(current_user: CurrentUser) -> uuid.UUID:
    """Extract organization ID from current user"""
    return current_user.organization_id


CurrentOrganization = Annotated[uuid.UUID, Depends(get_current_organization)]


def require_role(*allowed_roles: str):
    """
    Dependency to check if current user has one of the allowed roles.

    Usage:
        @router.get("/admin-only", dependencies=[Depends(require_role("admin"))])
        def admin_route(): ...

        @router.get("/sellers", dependencies=[Depends(require_role("admin", "seller"))])
        def seller_route(): ...
    """

    def role_checker(session: SessionDep, current_user: CurrentUser) -> User:
        # Get user's role
        role = session.get(Role, current_user.role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User role not found",
            )

        # Check if user has required role
        if role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(allowed_roles)}",
            )

        return current_user

    return role_checker


def get_current_admin_user(session: SessionDep, current_user: CurrentUser) -> User:
    """Dependency that requires admin role"""
    role = session.get(Role, current_user.role_id)
    if not role or role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


CurrentAdminUser = Annotated[User, Depends(get_current_admin_user)]

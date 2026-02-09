import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app import crud
from app.api.deps import SessionDep
from app.core.security import get_password_hash
from app.models import (
    User,
    UserPublic,
)

router = APIRouter(tags=["private"], prefix="/private")


class PrivateUserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    organization_id: uuid.UUID
    role_id: int = 3  # Default to viewer
    is_verified: bool = False


@router.post("/users/", response_model=UserPublic)
def create_user(user_in: PrivateUserCreate, session: SessionDep) -> Any:
    """
    Create a new user (internal/private endpoint).
    """
    # Validate organization exists
    organization = crud.get_organization_by_id(
        session=session, organization_id=user_in.organization_id
    )
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Validate role exists
    role = crud.get_role_by_id(session=session, role_id=user_in.role_id)
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role_id")

    user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        organization_id=user_in.organization_id,
        role_id=user_in.role_id,
        is_verified=user_in.is_verified,
        hashed_password=get_password_hash(user_in.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

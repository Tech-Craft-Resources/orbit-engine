import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import User, UserCreate, UserUpdate
from tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def _get_default_org_id(db: Session) -> uuid.UUID:
    """Get the default organization ID for tests."""
    org = crud.get_organization_by_slug(session=db, slug="default")
    if not org:
        raise RuntimeError("Default organization not found. Run init_db first.")
    return org.id


def _get_role_id(db: Session, role_name: str = "viewer") -> int:
    """Get a role ID for tests. Defaults to 'viewer' for normal users."""
    role = crud.get_role_by_name(session=db, name=role_name)
    if not role:
        raise RuntimeError(f"Role '{role_name}' not found. Run migrations first.")
    return role.id


def create_random_user(db: Session, role_name: str = "viewer") -> User:
    email = random_email()
    password = random_lower_string()
    organization_id = _get_default_org_id(db)
    role_id = _get_role_id(db, role_name)
    user_in = UserCreate(
        email=email,
        password=password,
        first_name="Test",
        last_name="User",
        role_id=role_id,
    )
    user = crud.create_user(
        session=db, user_create=user_in, organization_id=organization_id
    )
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.get_user_by_email(session=db, email=email)
    if not user:
        organization_id = _get_default_org_id(db)
        role_id = _get_role_id(db, "viewer")
        user_in_create = UserCreate(
            email=email,
            password=password,
            first_name="Test",
            last_name="User",
            role_id=role_id,
        )
        user = crud.create_user(
            session=db, user_create=user_in_create, organization_id=organization_id
        )
    else:
        # Directly update the password hash since UserUpdate doesn't have a password field
        user.hashed_password = get_password_hash(password)
        db.add(user)
        db.commit()
        db.refresh(user)

    return user_authentication_headers(client=client, email=email, password=password)

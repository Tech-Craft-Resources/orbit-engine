from fastapi.encoders import jsonable_encoder
from pwdlib.hashers.bcrypt import BcryptHasher
from sqlmodel import Session

from app import crud
from app.core.security import verify_password
from app.models import User, UserCreate, UserUpdate
from tests.utils.user import _get_default_org_id, _get_role_id
from tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organization_id = _get_default_org_id(db)
    role_id = _get_role_id(db, "viewer")
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
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organization_id = _get_default_org_id(db)
    role_id = _get_role_id(db, "viewer")
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
    authenticated_user = crud.authenticate(session=db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.authenticate(session=db, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organization_id = _get_default_org_id(db)
    role_id = _get_role_id(db, "viewer")
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
    assert user.is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organization_id = _get_default_org_id(db)
    role_id = _get_role_id(db, "viewer")
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
    # Deactivate the user after creation
    crud.update_user(session=db, db_user=user, user_in=UserUpdate(is_active=False))
    db.refresh(user)
    assert user.is_active is False


def test_user_role_is_admin(db: Session) -> None:
    """Test that a user created with admin role has the correct role_id."""
    email = random_email()
    password = random_lower_string()
    organization_id = _get_default_org_id(db)
    admin_role_id = _get_role_id(db, "admin")
    user_in = UserCreate(
        email=email,
        password=password,
        first_name="Admin",
        last_name="User",
        role_id=admin_role_id,
    )
    user = crud.create_user(
        session=db, user_create=user_in, organization_id=organization_id
    )
    assert user.role_id == admin_role_id


def test_user_role_is_viewer(db: Session) -> None:
    """Test that a user created with viewer role has the correct role_id."""
    email = random_email()
    password = random_lower_string()
    organization_id = _get_default_org_id(db)
    viewer_role_id = _get_role_id(db, "viewer")
    user_in = UserCreate(
        email=email,
        password=password,
        first_name="Normal",
        last_name="User",
        role_id=viewer_role_id,
    )
    user = crud.create_user(
        session=db, user_create=user_in, organization_id=organization_id
    )
    assert user.role_id == viewer_role_id


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    organization_id = _get_default_org_id(db)
    role_id = _get_role_id(db, "viewer")
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
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    organization_id = _get_default_org_id(db)
    role_id = _get_role_id(db, "viewer")
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
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, first_name="Updated")
    if user.id is not None:
        crud.update_user(session=db, db_user=user, user_in=user_in_update)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert user_2.first_name == "Updated"
    verified, _ = verify_password(new_password, user_2.hashed_password)
    assert verified


def test_authenticate_user_with_bcrypt_upgrades_to_argon2(db: Session) -> None:
    """Test that a user with bcrypt password hash gets upgraded to argon2 on login."""
    email = random_email()
    password = random_lower_string()
    organization_id = _get_default_org_id(db)
    role_id = _get_role_id(db, "viewer")

    # Create a bcrypt hash directly (simulating legacy password)
    bcrypt_hasher = BcryptHasher()
    bcrypt_hash = bcrypt_hasher.hash(password)
    assert bcrypt_hash.startswith("$2")  # bcrypt hashes start with $2

    # Create user with bcrypt hash directly in the database
    user = User(
        email=email,
        hashed_password=bcrypt_hash,
        first_name="Legacy",
        last_name="User",
        organization_id=organization_id,
        role_id=role_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Verify the hash is bcrypt before authentication
    assert user.hashed_password.startswith("$2")

    # Authenticate - this should upgrade the hash to argon2
    authenticated_user = crud.authenticate(session=db, email=email, password=password)
    assert authenticated_user
    assert authenticated_user.email == email

    db.refresh(authenticated_user)

    # Verify the hash was upgraded to argon2
    assert authenticated_user.hashed_password.startswith("$argon2")

    verified, updated_hash = verify_password(
        password, authenticated_user.hashed_password
    )
    assert verified
    # Should not need another update since it's already argon2
    assert updated_hash is None

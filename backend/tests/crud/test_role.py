from sqlmodel import Session

from app import crud

EXPECTED_ROLES = {"admin", "seller", "viewer"}


# ---------------------------------------------------------------------------
# get_roles
# ---------------------------------------------------------------------------


def test_get_roles_returns_all(db: Session) -> None:
    roles = crud.get_roles(session=db)
    assert len(roles) >= len(EXPECTED_ROLES)


def test_get_roles_contain_expected_names(db: Session) -> None:
    roles = crud.get_roles(session=db)
    role_names = {r.name for r in roles}
    assert EXPECTED_ROLES.issubset(role_names), (
        f"Missing roles: {EXPECTED_ROLES - role_names}"
    )


def test_get_roles_have_permissions_list(db: Session) -> None:
    roles = crud.get_roles(session=db)
    for role in roles:
        assert isinstance(role.permissions, list)


# ---------------------------------------------------------------------------
# get_role_by_name
# ---------------------------------------------------------------------------


def test_get_role_by_name_admin(db: Session) -> None:
    role = crud.get_role_by_name(session=db, name="admin")
    assert role is not None
    assert role.name == "admin"
    assert role.id is not None
    assert role.created_at is not None


def test_get_role_by_name_seller(db: Session) -> None:
    role = crud.get_role_by_name(session=db, name="seller")
    assert role is not None
    assert role.name == "seller"


def test_get_role_by_name_viewer(db: Session) -> None:
    role = crud.get_role_by_name(session=db, name="viewer")
    assert role is not None
    assert role.name == "viewer"


def test_get_role_by_name_not_found(db: Session) -> None:
    role = crud.get_role_by_name(session=db, name="nonexistent-role")
    assert role is None


# ---------------------------------------------------------------------------
# get_role_by_id
# ---------------------------------------------------------------------------


def test_get_role_by_id(db: Session) -> None:
    admin = crud.get_role_by_name(session=db, name="admin")
    assert admin is not None
    fetched = crud.get_role_by_id(session=db, role_id=admin.id)
    assert fetched is not None
    assert fetched.id == admin.id
    assert fetched.name == "admin"


def test_get_role_by_id_not_found(db: Session) -> None:
    result = crud.get_role_by_id(session=db, role_id=99999)
    assert result is None


# ---------------------------------------------------------------------------
# Role uniqueness (data integrity)
# ---------------------------------------------------------------------------


def test_roles_have_unique_names(db: Session) -> None:
    roles = crud.get_roles(session=db)
    names = [r.name for r in roles]
    assert len(names) == len(set(names)), "Role names must be unique"


def test_roles_have_unique_ids(db: Session) -> None:
    roles = crud.get_roles(session=db)
    ids = [r.id for r in roles]
    assert len(ids) == len(set(ids)), "Role IDs must be unique"

import uuid

from sqlmodel import Session

from app import crud
from app.models import OrganizationCreate, OrganizationUpdate
from tests.utils.utils import random_lower_string


def _random_slug() -> str:
    return f"org-{random_lower_string()[:12]}"


def _create_org(db: Session, slug: str | None = None) -> object:
    org_in = OrganizationCreate(
        name=f"Org {random_lower_string()[:16]}",
        slug=slug or _random_slug(),
    )
    return crud.create_organization(session=db, organization_create=org_in)


# ---------------------------------------------------------------------------
# create_organization
# ---------------------------------------------------------------------------


def test_create_organization(db: Session) -> None:
    slug = _random_slug()
    org_in = OrganizationCreate(name="Test Org", slug=slug)
    org = crud.create_organization(session=db, organization_create=org_in)
    assert org.id is not None
    assert org.name == "Test Org"
    assert org.slug == slug
    assert org.is_active is True


def test_create_organization_with_description(db: Session) -> None:
    org_in = OrganizationCreate(
        name="Org With Desc",
        slug=_random_slug(),
        description="A test description",
    )
    org = crud.create_organization(session=db, organization_create=org_in)
    assert org.description == "A test description"


def test_create_organization_defaults_active(db: Session) -> None:
    org = _create_org(db)
    assert org.is_active is True  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# get_organization_by_id
# ---------------------------------------------------------------------------


def test_get_organization_by_id(db: Session) -> None:
    org = _create_org(db)
    fetched = crud.get_organization_by_id(session=db, organization_id=org.id)  # type: ignore[arg-type]
    assert fetched is not None
    assert fetched.id == org.id  # type: ignore[union-attr]
    assert fetched.slug == org.slug  # type: ignore[union-attr]


def test_get_organization_by_id_not_found(db: Session) -> None:
    result = crud.get_organization_by_id(session=db, organization_id=uuid.uuid4())
    assert result is None


# ---------------------------------------------------------------------------
# get_organization_by_slug
# ---------------------------------------------------------------------------


def test_get_organization_by_slug(db: Session) -> None:
    slug = _random_slug()
    _create_org(db, slug=slug)
    fetched = crud.get_organization_by_slug(session=db, slug=slug)
    assert fetched is not None
    assert fetched.slug == slug  # type: ignore[union-attr]


def test_get_organization_by_slug_not_found(db: Session) -> None:
    result = crud.get_organization_by_slug(session=db, slug="nonexistent-slug-xyz")
    assert result is None


# ---------------------------------------------------------------------------
# update_organization
# ---------------------------------------------------------------------------


def test_update_organization_name(db: Session) -> None:
    org = _create_org(db)
    update = OrganizationUpdate(name="Renamed Org")
    updated = crud.update_organization(session=db, db_organization=org, organization_in=update)  # type: ignore[arg-type]
    assert updated.name == "Renamed Org"


def test_update_organization_description(db: Session) -> None:
    org = _create_org(db)
    update = OrganizationUpdate(description="New description")
    updated = crud.update_organization(session=db, db_organization=org, organization_in=update)  # type: ignore[arg-type]
    assert updated.description == "New description"


def test_update_organization_slug(db: Session) -> None:
    org = _create_org(db)
    new_slug = _random_slug()
    update = OrganizationUpdate(slug=new_slug)
    updated = crud.update_organization(session=db, db_organization=org, organization_in=update)  # type: ignore[arg-type]
    assert updated.slug == new_slug


def test_update_organization_partial(db: Session) -> None:
    """Only provided fields are updated; others remain unchanged."""
    org = _create_org(db)
    original_slug = org.slug  # type: ignore[union-attr]
    update = OrganizationUpdate(name="Partial Update")
    updated = crud.update_organization(session=db, db_organization=org, organization_in=update)  # type: ignore[arg-type]
    assert updated.name == "Partial Update"
    assert updated.slug == original_slug


def test_update_organization_deactivate(db: Session) -> None:
    org = _create_org(db)
    update = OrganizationUpdate(is_active=False)
    updated = crud.update_organization(session=db, db_organization=org, organization_in=update)  # type: ignore[arg-type]
    assert updated.is_active is False

from sqlmodel import Session

from app import crud
from app.models import CategoryCreate, CategoryUpdate
from tests.utils.category import create_random_category
from tests.utils.user import _get_default_org_id
from tests.utils.utils import random_lower_string


def test_create_category(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    name = f"Cat-{random_lower_string()[:16]}"
    category_in = CategoryCreate(name=name, description="Test desc")
    category = crud.create_category(
        session=db, category_create=category_in, organization_id=organization_id
    )
    assert category.name == name
    assert category.description == "Test desc"
    assert category.organization_id == organization_id
    assert category.is_active is True
    assert category.deleted_at is None


def test_create_category_with_parent(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    parent = create_random_category(db, organization_id=organization_id)
    child_name = f"Child-{random_lower_string()[:16]}"
    category_in = CategoryCreate(name=child_name, parent_id=parent.id)
    child = crud.create_category(
        session=db, category_create=category_in, organization_id=organization_id
    )
    assert child.parent_id == parent.id
    assert child.name == child_name


def test_get_category_by_id(db: Session) -> None:
    category = create_random_category(db)
    fetched = crud.get_category_by_id(
        session=db,
        category_id=category.id,
        organization_id=category.organization_id,
    )
    assert fetched
    assert fetched.id == category.id
    assert fetched.name == category.name


def test_get_category_by_id_not_found(db: Session) -> None:
    import uuid

    organization_id = _get_default_org_id(db)
    fetched = crud.get_category_by_id(
        session=db,
        category_id=uuid.uuid4(),
        organization_id=organization_id,
    )
    assert fetched is None


def test_get_categories_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    # Create a few categories
    create_random_category(db, organization_id=organization_id)
    create_random_category(db, organization_id=organization_id)
    categories = crud.get_categories_by_organization(
        session=db, organization_id=organization_id
    )
    assert len(categories) >= 2


def test_count_categories_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    count = crud.count_categories_by_organization(
        session=db, organization_id=organization_id
    )
    assert count >= 0


def test_get_category_by_name(db: Session) -> None:
    category = create_random_category(db)
    fetched = crud.get_category_by_name(
        session=db,
        name=category.name,
        organization_id=category.organization_id,
        parent_id=category.parent_id,
    )
    assert fetched
    assert fetched.id == category.id


def test_update_category(db: Session) -> None:
    category = create_random_category(db)
    new_name = f"Updated-{random_lower_string()[:16]}"
    update_data = CategoryUpdate(name=new_name, description="Updated desc")
    updated = crud.update_category(
        session=db, db_category=category, category_in=update_data
    )
    assert updated.name == new_name
    assert updated.description == "Updated desc"


def test_soft_delete_category(db: Session) -> None:
    category = create_random_category(db)
    deleted = crud.soft_delete_category(session=db, db_category=category)
    assert deleted.deleted_at is not None
    assert deleted.is_active is False

    # Should not appear in normal queries
    fetched = crud.get_category_by_id(
        session=db,
        category_id=category.id,
        organization_id=category.organization_id,
    )
    assert fetched is None

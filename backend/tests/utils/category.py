import uuid

from sqlmodel import Session

from app import crud
from app.models import Category, CategoryCreate
from tests.utils.user import _get_default_org_id
from tests.utils.utils import random_lower_string


def create_random_category(
    db: Session,
    *,
    organization_id: uuid.UUID | None = None,
    parent_id: uuid.UUID | None = None,
) -> Category:
    """Create a random category for testing."""
    if organization_id is None:
        organization_id = _get_default_org_id(db)
    category_in = CategoryCreate(
        name=f"Category-{random_lower_string()[:16]}",
        description="Test category",
        parent_id=parent_id,
    )
    return crud.create_category(
        session=db, category_create=category_in, organization_id=organization_id
    )

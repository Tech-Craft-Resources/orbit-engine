import uuid
from decimal import Decimal

from sqlmodel import Session

from app import crud
from app.models import Product, ProductCreate
from tests.utils.user import _get_default_org_id
from tests.utils.utils import random_lower_string


def create_random_product(
    db: Session,
    *,
    organization_id: uuid.UUID | None = None,
    category_id: uuid.UUID | None = None,
    stock_quantity: int = 100,
    stock_min: int = 10,
) -> Product:
    """Create a random product for testing."""
    if organization_id is None:
        organization_id = _get_default_org_id(db)
    sku = f"SKU-{random_lower_string()[:16]}"
    product_in = ProductCreate(
        name=f"Product-{random_lower_string()[:16]}",
        sku=sku,
        description="Test product",
        cost_price=Decimal("10.00"),
        sale_price=Decimal("25.00"),
        stock_quantity=stock_quantity,
        stock_min=stock_min,
        category_id=category_id,
    )
    return crud.create_product(
        session=db, product_create=product_in, organization_id=organization_id
    )

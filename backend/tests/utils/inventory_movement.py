import uuid

from sqlmodel import Session

from app import crud
from app.models import InventoryMovement, InventoryMovementCreate
from tests.utils.product import create_random_product
from tests.utils.user import _get_default_org_id, create_random_user


def create_random_movement(
    db: Session,
    *,
    organization_id: uuid.UUID | None = None,
    product_id: uuid.UUID | None = None,
    user_id: uuid.UUID | None = None,
    movement_type: str = "adjustment",
    quantity: int = 10,
) -> InventoryMovement:
    """Create a random inventory movement for testing."""
    if organization_id is None:
        organization_id = _get_default_org_id(db)

    if product_id is None:
        product = create_random_product(
            db, organization_id=organization_id, stock_quantity=100
        )
        product_id = product.id
    else:
        product = crud.get_product_by_id(
            session=db, product_id=product_id, organization_id=organization_id
        )

    if user_id is None:
        user = create_random_user(db, role_name="seller")
        user_id = user.id

    assert product is not None
    previous_stock = product.stock_quantity
    new_stock = previous_stock + quantity

    # Adjust product stock
    crud.adjust_product_stock(session=db, db_product=product, quantity=quantity)

    movement_in = InventoryMovementCreate(
        product_id=product_id,
        movement_type=movement_type,
        quantity=quantity,
        reason="Test movement",
    )
    return crud.create_inventory_movement(
        session=db,
        movement_create=movement_in,
        organization_id=organization_id,
        user_id=user_id,
        previous_stock=previous_stock,
        new_stock=new_stock,
    )

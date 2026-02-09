import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.deps import (
    CurrentOrganization,
    CurrentUser,
    SessionDep,
    require_role,
)
from app.models import (
    InventoryMovementCreate,
    InventoryMovementPublic,
    InventoryMovementsPublic,
)

router = APIRouter()


@router.get("/", response_model=InventoryMovementsPublic)
def read_movements(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve inventory movements in current organization.

    Any authenticated user can list movements.
    """
    movements = crud.get_movements_by_organization(
        session=session, organization_id=current_organization, skip=skip, limit=limit
    )
    count = crud.count_movements_by_organization(
        session=session, organization_id=current_organization
    )
    return InventoryMovementsPublic(data=movements, count=count)


@router.post(
    "/",
    response_model=InventoryMovementPublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def create_movement(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    movement_in: InventoryMovementCreate,
) -> Any:
    """
    Create a manual inventory movement (purchase, adjustment, return).

    Only admin and seller roles can create movements.
    Movement types 'sale' cannot be created directly; they are created
    automatically when a sale is recorded.
    """
    # Validate movement_type
    allowed_types = {"purchase", "adjustment", "return"}
    if movement_in.movement_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid movement type. Allowed types: {', '.join(sorted(allowed_types))}",
        )

    # Validate product exists
    product = crud.get_product_by_id(
        session=session,
        product_id=movement_in.product_id,
        organization_id=current_organization,
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check that stock won't go negative
    new_stock = product.stock_quantity + movement_in.quantity
    if new_stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Stock quantity cannot be negative after this movement",
        )

    previous_stock = product.stock_quantity

    # Adjust product stock
    crud.adjust_product_stock(
        session=session, db_product=product, quantity=movement_in.quantity
    )

    # Create movement record
    movement = crud.create_inventory_movement(
        session=session,
        movement_create=movement_in,
        organization_id=current_organization,
        user_id=current_user.id,
        previous_stock=previous_stock,
        new_stock=new_stock,
    )
    return movement


@router.get("/{movement_id}", response_model=InventoryMovementPublic)
def read_movement(
    movement_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Get a specific inventory movement by ID.

    Any authenticated user can view a movement.
    """
    movement = crud.get_inventory_movement_by_id(
        session=session,
        movement_id=movement_id,
        organization_id=current_organization,
    )
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement

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
    Message,
    ProductCreate,
    ProductPublic,
    ProductsPublic,
    ProductUpdate,
    StockAdjustment,
    InventoryMovementsPublic,
)

router = APIRouter()


@router.get("/", response_model=ProductsPublic)
def read_products(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve products in current organization.

    Any authenticated user can list products.
    """
    products = crud.get_products_by_organization(
        session=session, organization_id=current_organization, skip=skip, limit=limit
    )
    count = crud.count_products_by_organization(
        session=session, organization_id=current_organization
    )
    return ProductsPublic(data=products, count=count)


@router.post(
    "/",
    response_model=ProductPublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def create_product(
    *,
    session: SessionDep,
    current_organization: CurrentOrganization,
    product_in: ProductCreate,
) -> Any:
    """
    Create a new product in current organization.

    Only admin and seller roles can create products.
    """
    # Validate category_id if provided
    if product_in.category_id is not None:
        category = crud.get_category_by_id(
            session=session,
            category_id=product_in.category_id,
            organization_id=current_organization,
        )
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

    # Check for duplicate SKU within organization
    existing = crud.get_product_by_sku(
        session=session,
        sku=product_in.sku,
        organization_id=current_organization,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A product with this SKU already exists in the organization",
        )

    product = crud.create_product(
        session=session,
        product_create=product_in,
        organization_id=current_organization,
    )
    return product


@router.get("/low-stock", response_model=ProductsPublic)
def read_low_stock_products(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve products with stock at or below minimum level.

    Any authenticated user can view low-stock products.
    """
    products = crud.get_low_stock_products(
        session=session, organization_id=current_organization, skip=skip, limit=limit
    )
    count = crud.count_low_stock_products(
        session=session, organization_id=current_organization
    )
    return ProductsPublic(data=products, count=count)


@router.get("/{product_id}", response_model=ProductPublic)
def read_product(
    product_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Get a specific product by ID.

    Any authenticated user can view a product.
    """
    product = crud.get_product_by_id(
        session=session,
        product_id=product_id,
        organization_id=current_organization,
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch(
    "/{product_id}",
    response_model=ProductPublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def update_product(
    *,
    session: SessionDep,
    current_organization: CurrentOrganization,
    product_id: uuid.UUID,
    product_in: ProductUpdate,
) -> Any:
    """
    Update a product.

    Only admin and seller roles can update products.
    """
    db_product = crud.get_product_by_id(
        session=session,
        product_id=product_id,
        organization_id=current_organization,
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Validate category_id if provided
    if product_in.category_id is not None:
        category = crud.get_category_by_id(
            session=session,
            category_id=product_in.category_id,
            organization_id=current_organization,
        )
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

    # Check for duplicate SKU if SKU is being changed
    if product_in.sku is not None and product_in.sku != db_product.sku:
        existing = crud.get_product_by_sku(
            session=session,
            sku=product_in.sku,
            organization_id=current_organization,
        )
        if existing:
            raise HTTPException(
                status_code=409,
                detail="A product with this SKU already exists in the organization",
            )

    product = crud.update_product(
        session=session, db_product=db_product, product_in=product_in
    )
    return product


@router.delete(
    "/{product_id}",
    response_model=Message,
    dependencies=[Depends(require_role("admin"))],
)
def delete_product(
    product_id: uuid.UUID,
    session: SessionDep,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Delete a product (soft delete).

    Only admin users can delete products.
    """
    db_product = crud.get_product_by_id(
        session=session,
        product_id=product_id,
        organization_id=current_organization,
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    crud.soft_delete_product(session=session, db_product=db_product)
    return Message(message="Product deleted successfully")


@router.post(
    "/{product_id}/adjust-stock",
    response_model=ProductPublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def adjust_stock(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    product_id: uuid.UUID,
    adjustment: StockAdjustment,
) -> Any:
    """
    Adjust product stock quantity.

    Only admin and seller roles can adjust stock.
    The quantity can be positive (add stock) or negative (subtract stock).
    Creates an inventory movement record for audit trail.
    """
    db_product = crud.get_product_by_id(
        session=session,
        product_id=product_id,
        organization_id=current_organization,
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ensure stock doesn't go negative
    new_stock = db_product.stock_quantity + adjustment.quantity
    if new_stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Stock quantity cannot be negative",
        )

    previous_stock = db_product.stock_quantity

    product = crud.adjust_product_stock(
        session=session, db_product=db_product, quantity=adjustment.quantity
    )

    # Create inventory movement record
    movement_create = InventoryMovementCreate(
        product_id=product_id,
        movement_type="adjustment",
        quantity=adjustment.quantity,
        reason=adjustment.reason,
    )
    crud.create_inventory_movement(
        session=session,
        movement_create=movement_create,
        organization_id=current_organization,
        user_id=current_user.id,
        previous_stock=previous_stock,
        new_stock=new_stock,
    )

    return product


@router.get("/{product_id}/movements", response_model=InventoryMovementsPublic)
def read_product_movements(
    product_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve inventory movements for a specific product.

    Any authenticated user can view product movements.
    """
    # Validate product exists
    product = crud.get_product_by_id(
        session=session,
        product_id=product_id,
        organization_id=current_organization,
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    movements = crud.get_movements_by_product(
        session=session,
        product_id=product_id,
        organization_id=current_organization,
        skip=skip,
        limit=limit,
    )
    count = crud.count_movements_by_product(
        session=session,
        product_id=product_id,
        organization_id=current_organization,
    )
    return InventoryMovementsPublic(data=movements, count=count)

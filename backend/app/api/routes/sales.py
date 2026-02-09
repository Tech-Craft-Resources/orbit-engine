import uuid
from decimal import Decimal
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
    SaleCancelRequest,
    SaleCreate,
    SalePublic,
    SalesPublic,
    SaleStatsPublic,
)

router = APIRouter()


@router.get("/", response_model=SalesPublic)
def read_sales(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve sales in current organization.

    Any authenticated user can list sales.
    """
    sales = crud.get_sales_by_organization(
        session=session, organization_id=current_organization, skip=skip, limit=limit
    )
    count = crud.count_sales_by_organization(
        session=session, organization_id=current_organization
    )
    return SalesPublic(data=sales, count=count)


@router.post(
    "/",
    response_model=SalePublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def create_sale(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    sale_in: SaleCreate,
) -> Any:
    """
    Create a new sale.

    Only admin and seller roles can create sales.
    This endpoint:
    - Validates all products exist and have sufficient stock
    - Calculates subtotal, total
    - Deducts stock from each product
    - Creates inventory movement records (type: sale)
    - Updates customer purchase stats if customer_id is provided
    - Generates a unique invoice number
    """
    # Validate customer if provided
    db_customer = None
    if sale_in.customer_id is not None:
        db_customer = crud.get_customer_by_id(
            session=session,
            customer_id=sale_in.customer_id,
            organization_id=current_organization,
        )
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

    # Validate all products and check stock
    product_map: dict[uuid.UUID, Any] = {}
    for item in sale_in.items:
        product = crud.get_product_by_id(
            session=session,
            product_id=item.product_id,
            organization_id=current_organization,
        )
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found",
            )
        if not product.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"Product '{product.name}' is not active",
            )
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}'. "
                f"Available: {product.stock_quantity}, Requested: {item.quantity}",
            )
        product_map[item.product_id] = product

    # Calculate subtotal from items
    subtotal = Decimal("0")
    for item in sale_in.items:
        product = product_map[item.product_id]
        item_subtotal = product.sale_price * item.quantity
        subtotal += item_subtotal

    # Calculate total
    total = subtotal - sale_in.discount + sale_in.tax
    if total < 0:
        total = Decimal("0")

    # Generate invoice number
    invoice_number = crud.generate_invoice_number(
        session=session, organization_id=current_organization
    )

    # Create the sale
    sale = crud.create_sale(
        session=session,
        organization_id=current_organization,
        user_id=current_user.id,
        customer_id=sale_in.customer_id,
        invoice_number=invoice_number,
        subtotal=subtotal,
        discount=sale_in.discount,
        tax=sale_in.tax,
        total=total,
        payment_method=sale_in.payment_method,
        notes=sale_in.notes,
    )

    # Create sale items, deduct stock, and create inventory movements
    for item in sale_in.items:
        product = product_map[item.product_id]
        item_subtotal = product.sale_price * item.quantity

        # Create sale item with snapshot data
        crud.create_sale_item(
            session=session,
            sale_id=sale.id,
            product_id=item.product_id,
            product_name=product.name,
            product_sku=product.sku,
            quantity=item.quantity,
            unit_price=product.sale_price,
            subtotal=item_subtotal,
        )

        # Deduct stock
        previous_stock = product.stock_quantity
        crud.adjust_product_stock(
            session=session, db_product=product, quantity=-item.quantity
        )
        new_stock = product.stock_quantity

        # Create inventory movement
        movement_create = InventoryMovementCreate(
            product_id=item.product_id,
            movement_type="sale",
            quantity=-item.quantity,
            reference_id=sale.id,
            reference_type="sale",
            reason=f"Sale {invoice_number}",
        )
        crud.create_inventory_movement(
            session=session,
            movement_create=movement_create,
            organization_id=current_organization,
            user_id=current_user.id,
            previous_stock=previous_stock,
            new_stock=new_stock,
        )

    # Update customer purchase stats
    if db_customer is not None:
        crud.update_customer_purchase_stats(
            session=session, db_customer=db_customer, sale_total=total
        )

    # Refresh sale to include items
    session.refresh(sale)
    return sale


@router.get("/today", response_model=SalesPublic)
def read_sales_today(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve today's completed sales.

    Any authenticated user can view today's sales.
    """
    sales = crud.get_sales_today(
        session=session, organization_id=current_organization, skip=skip, limit=limit
    )
    count = crud.count_sales_today(
        session=session, organization_id=current_organization
    )
    return SalesPublic(data=sales, count=count)


@router.get("/stats", response_model=SaleStatsPublic)
def read_sales_stats(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Get sales statistics for the current organization.

    Any authenticated user can view sales stats.
    """
    stats = crud.get_sales_stats(
        session=session, organization_id=current_organization
    )
    return SaleStatsPublic(**stats)


@router.get("/{sale_id}", response_model=SalePublic)
def read_sale(
    sale_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Get a specific sale by ID, including its items.

    Any authenticated user can view a sale.
    """
    sale = crud.get_sale_by_id(
        session=session,
        sale_id=sale_id,
        organization_id=current_organization,
    )
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.post(
    "/{sale_id}/cancel",
    response_model=SalePublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def cancel_sale(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    sale_id: uuid.UUID,
    cancel_request: SaleCancelRequest,
) -> Any:
    """
    Cancel a sale.

    Only admin and seller roles can cancel sales.
    This endpoint:
    - Validates the sale exists and is not already cancelled
    - Restores stock for each sale item
    - Creates inventory movement records (type: return)
    - Reverts customer purchase stats if customer_id is set
    """
    sale = crud.get_sale_by_id(
        session=session,
        sale_id=sale_id,
        organization_id=current_organization,
    )
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    if sale.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Sale is already cancelled",
        )

    # Get sale items to restore stock
    sale_items = crud.get_sale_items(session=session, sale_id=sale.id)

    for item in sale_items:
        # Restore stock
        product = crud.get_product_by_id(
            session=session,
            product_id=item.product_id,
            organization_id=current_organization,
        )
        if product:
            previous_stock = product.stock_quantity
            crud.adjust_product_stock(
                session=session, db_product=product, quantity=item.quantity
            )
            new_stock = product.stock_quantity

            # Create return movement
            movement_create = InventoryMovementCreate(
                product_id=item.product_id,
                movement_type="return",
                quantity=item.quantity,
                reference_id=sale.id,
                reference_type="sale",
                reason=f"Sale {sale.invoice_number} cancelled: {cancel_request.reason}",
            )
            crud.create_inventory_movement(
                session=session,
                movement_create=movement_create,
                organization_id=current_organization,
                user_id=current_user.id,
                previous_stock=previous_stock,
                new_stock=new_stock,
            )

    # Revert customer purchase stats
    if sale.customer_id is not None:
        db_customer = crud.get_customer_by_id(
            session=session,
            customer_id=sale.customer_id,
            organization_id=current_organization,
        )
        if db_customer:
            crud.revert_customer_purchase_stats(
                session=session, db_customer=db_customer, sale_total=sale.total
            )

    # Cancel the sale
    cancelled_sale = crud.cancel_sale(
        session=session,
        db_sale=sale,
        cancelled_by=current_user.id,
        reason=cancel_request.reason,
    )
    return cancelled_sale

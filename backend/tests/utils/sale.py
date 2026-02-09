import uuid
from decimal import Decimal

from sqlmodel import Session

from app import crud
from app.models import Sale
from tests.utils.customer import create_random_customer
from tests.utils.product import create_random_product
from tests.utils.user import _get_default_org_id, create_random_user


def create_random_sale(
    db: Session,
    *,
    organization_id: uuid.UUID | None = None,
    customer_id: uuid.UUID | None = None,
    user_id: uuid.UUID | None = None,
    with_customer: bool = True,
    num_items: int = 1,
    stock_quantity: int = 100,
) -> Sale:
    """Create a random sale with items for testing."""
    if organization_id is None:
        organization_id = _get_default_org_id(db)

    if with_customer and customer_id is None:
        customer = create_random_customer(db, organization_id=organization_id)
        customer_id = customer.id

    if user_id is None:
        user = create_random_user(db, role_name="seller")
        user_id = user.id

    # Generate invoice number
    invoice_number = crud.generate_invoice_number(
        session=db, organization_id=organization_id
    )

    # Create products and calculate totals
    subtotal = Decimal("0")
    products_data = []
    for _ in range(num_items):
        product = create_random_product(
            db, organization_id=organization_id, stock_quantity=stock_quantity
        )
        item_quantity = 2
        item_subtotal = product.sale_price * item_quantity
        subtotal += item_subtotal
        products_data.append(
            {
                "product": product,
                "quantity": item_quantity,
                "unit_price": product.sale_price,
                "subtotal": item_subtotal,
            }
        )

    total = subtotal  # No discount/tax for simplicity

    # Create the sale
    sale = crud.create_sale(
        session=db,
        organization_id=organization_id,
        user_id=user_id,
        customer_id=customer_id,
        invoice_number=invoice_number,
        subtotal=subtotal,
        discount=Decimal("0"),
        tax=Decimal("0"),
        total=total,
        payment_method="cash",
        notes=None,
    )

    # Create sale items and deduct stock
    for data in products_data:
        product = data["product"]
        crud.create_sale_item(
            session=db,
            sale_id=sale.id,
            product_id=product.id,
            product_name=product.name,
            product_sku=product.sku,
            quantity=data["quantity"],
            unit_price=data["unit_price"],
            subtotal=data["subtotal"],
        )
        # Deduct stock
        crud.adjust_product_stock(
            session=db, db_product=product, quantity=-data["quantity"]
        )

    # Update customer purchase stats if customer was provided
    if customer_id is not None:
        customer_obj = crud.get_customer_by_id(
            session=db, customer_id=customer_id, organization_id=organization_id
        )
        if customer_obj:
            crud.update_customer_purchase_stats(
                session=db, db_customer=customer_obj, sale_total=total
            )

    db.refresh(sale)
    return sale

import uuid
from decimal import Decimal

from sqlmodel import Session

from app import crud
from tests.utils.customer import create_random_customer
from tests.utils.product import create_random_product
from tests.utils.sale import create_random_sale
from tests.utils.user import _get_default_org_id, create_random_user


def test_generate_invoice_number(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    invoice1 = crud.generate_invoice_number(
        session=db, organization_id=organization_id
    )
    assert invoice1.startswith("INV-")
    assert len(invoice1) == 10  # INV-XXXXXX


def test_generate_invoice_number_sequential(db: Session) -> None:
    """Invoice numbers should be sequential per organization."""
    organization_id = _get_default_org_id(db)
    # Create a sale to advance the counter
    create_random_sale(db, organization_id=organization_id)
    inv1 = crud.generate_invoice_number(
        session=db, organization_id=organization_id
    )
    create_random_sale(db, organization_id=organization_id)
    inv2 = crud.generate_invoice_number(
        session=db, organization_id=organization_id
    )
    # Extract numbers and verify sequential
    num1 = int(inv1.split("-")[1])
    num2 = int(inv2.split("-")[1])
    assert num2 > num1


def test_create_sale(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    user = create_random_user(db, role_name="seller")
    customer = create_random_customer(db, organization_id=organization_id)
    invoice_number = crud.generate_invoice_number(
        session=db, organization_id=organization_id
    )
    sale = crud.create_sale(
        session=db,
        organization_id=organization_id,
        user_id=user.id,
        customer_id=customer.id,
        invoice_number=invoice_number,
        subtotal=Decimal("100.00"),
        discount=Decimal("5.00"),
        tax=Decimal("10.00"),
        total=Decimal("105.00"),
        payment_method="cash",
        notes="Test sale",
    )
    assert sale.id is not None
    assert sale.organization_id == organization_id
    assert sale.user_id == user.id
    assert sale.customer_id == customer.id
    assert sale.invoice_number == invoice_number
    assert sale.subtotal == Decimal("100.00")
    assert sale.discount == Decimal("5.00")
    assert sale.tax == Decimal("10.00")
    assert sale.total == Decimal("105.00")
    assert sale.payment_method == "cash"
    assert sale.status == "completed"
    assert sale.notes == "Test sale"
    assert sale.created_at is not None


def test_create_sale_without_customer(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    user = create_random_user(db, role_name="seller")
    invoice_number = crud.generate_invoice_number(
        session=db, organization_id=organization_id
    )
    sale = crud.create_sale(
        session=db,
        organization_id=organization_id,
        user_id=user.id,
        customer_id=None,
        invoice_number=invoice_number,
        subtotal=Decimal("50.00"),
        discount=Decimal("0"),
        tax=Decimal("0"),
        total=Decimal("50.00"),
        payment_method="card",
        notes=None,
    )
    assert sale.customer_id is None
    assert sale.payment_method == "card"


def test_create_sale_item(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    sale = create_random_sale(db, organization_id=organization_id, with_customer=False)
    product = create_random_product(db, organization_id=organization_id)
    item = crud.create_sale_item(
        session=db,
        sale_id=sale.id,
        product_id=product.id,
        product_name=product.name,
        product_sku=product.sku,
        quantity=3,
        unit_price=Decimal("25.00"),
        subtotal=Decimal("75.00"),
    )
    assert item.id is not None
    assert item.sale_id == sale.id
    assert item.product_id == product.id
    assert item.product_name == product.name
    assert item.product_sku == product.sku
    assert item.quantity == 3
    assert item.unit_price == Decimal("25.00")
    assert item.subtotal == Decimal("75.00")
    assert item.created_at is not None


def test_get_sale_by_id(db: Session) -> None:
    sale = create_random_sale(db)
    fetched = crud.get_sale_by_id(
        session=db,
        sale_id=sale.id,
        organization_id=sale.organization_id,
    )
    assert fetched is not None
    assert fetched.id == sale.id
    assert fetched.invoice_number == sale.invoice_number


def test_get_sale_by_id_not_found(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    fetched = crud.get_sale_by_id(
        session=db,
        sale_id=uuid.uuid4(),
        organization_id=organization_id,
    )
    assert fetched is None


def test_get_sales_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id)
    create_random_sale(db, organization_id=organization_id)
    sales = crud.get_sales_by_organization(
        session=db, organization_id=organization_id
    )
    assert len(sales) >= 2


def test_count_sales_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    count = crud.count_sales_by_organization(
        session=db, organization_id=organization_id
    )
    assert count >= 0


def test_get_sale_items(db: Session) -> None:
    sale = create_random_sale(db, num_items=2)
    items = crud.get_sale_items(session=db, sale_id=sale.id)
    assert len(items) == 2


def test_cancel_sale(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    user = create_random_user(db, role_name="admin")
    sale = create_random_sale(db, organization_id=organization_id)
    cancelled = crud.cancel_sale(
        session=db,
        db_sale=sale,
        cancelled_by=user.id,
        reason="Customer requested cancellation",
    )
    assert cancelled.status == "cancelled"
    assert cancelled.cancelled_by == user.id
    assert cancelled.cancellation_reason == "Customer requested cancellation"
    assert cancelled.cancelled_at is not None


def test_get_sales_today(db: Session) -> None:
    """Sales created now should appear in today's sales."""
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id)
    sales = crud.get_sales_today(
        session=db, organization_id=organization_id
    )
    assert len(sales) >= 1


def test_count_sales_today(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    count = crud.count_sales_today(
        session=db, organization_id=organization_id
    )
    assert count >= 0


def test_get_sales_stats(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id)
    stats = crud.get_sales_stats(
        session=db, organization_id=organization_id
    )
    assert "sales_today_count" in stats
    assert "sales_today_total" in stats
    assert "sales_month_count" in stats
    assert "sales_month_total" in stats
    assert "average_ticket" in stats
    assert stats["sales_today_count"] >= 1
    assert stats["sales_month_count"] >= 1


def test_update_customer_purchase_stats(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    customer = create_random_customer(db, organization_id=organization_id)
    initial_count = customer.purchases_count
    initial_total = customer.total_purchases

    crud.update_customer_purchase_stats(
        session=db, db_customer=customer, sale_total=Decimal("150.00")
    )
    assert customer.purchases_count == initial_count + 1
    assert customer.total_purchases == Decimal(str(initial_total)) + Decimal("150.00")
    assert customer.last_purchase_at is not None


def test_revert_customer_purchase_stats(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    customer = create_random_customer(db, organization_id=organization_id)

    # First add stats
    crud.update_customer_purchase_stats(
        session=db, db_customer=customer, sale_total=Decimal("100.00")
    )
    assert customer.purchases_count == 1

    # Then revert
    crud.revert_customer_purchase_stats(
        session=db, db_customer=customer, sale_total=Decimal("100.00")
    )
    assert customer.purchases_count == 0
    assert customer.total_purchases == Decimal("0")


def test_revert_customer_purchase_stats_no_negative(db: Session) -> None:
    """Reverting stats should not go below zero."""
    organization_id = _get_default_org_id(db)
    customer = create_random_customer(db, organization_id=organization_id)

    crud.revert_customer_purchase_stats(
        session=db, db_customer=customer, sale_total=Decimal("100.00")
    )
    assert customer.purchases_count == 0
    assert customer.total_purchases == Decimal("0")


def test_get_sales_by_customer(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    customer = create_random_customer(db, organization_id=organization_id)
    create_random_sale(db, organization_id=organization_id, customer_id=customer.id)
    create_random_sale(db, organization_id=organization_id, customer_id=customer.id)
    sales = crud.get_sales_by_customer(
        session=db,
        customer_id=customer.id,
        organization_id=organization_id,
    )
    assert len(sales) >= 2


def test_count_sales_by_customer(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    customer = create_random_customer(db, organization_id=organization_id)
    create_random_sale(db, organization_id=organization_id, customer_id=customer.id)
    count = crud.count_sales_by_customer(
        session=db,
        customer_id=customer.id,
        organization_id=organization_id,
    )
    assert count >= 1


def test_sales_ordered_by_most_recent(db: Session) -> None:
    """Sales should be returned ordered by created_at desc."""
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id)
    create_random_sale(db, organization_id=organization_id)
    sales = crud.get_sales_by_organization(
        session=db, organization_id=organization_id
    )
    assert len(sales) >= 2
    assert sales[0].created_at >= sales[1].created_at

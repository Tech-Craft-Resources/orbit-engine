from decimal import Decimal

from sqlmodel import Session

from app import crud
from tests.utils.product import create_random_product
from tests.utils.sale import create_random_sale
from tests.utils.user import _get_default_org_id


# ---------------------------------------------------------------------------
# get_top_products
# ---------------------------------------------------------------------------


def test_get_top_products(db: Session) -> None:
    """Top products should include products from completed sales."""
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id, num_items=2)
    top = crud.get_top_products(session=db, organization_id=organization_id)
    assert isinstance(top, list)
    assert len(top) >= 1
    item = top[0]
    assert "product_id" in item
    assert "product_name" in item
    assert "quantity_sold" in item
    assert "revenue" in item
    assert item["quantity_sold"] > 0
    assert item["revenue"] > Decimal("0")


def test_get_top_products_empty(db: Session) -> None:
    """Top products for an org with no sales should return an empty list."""
    import uuid

    # Use a random UUID that doesn't match any organization
    fake_org_id = uuid.uuid4()
    top = crud.get_top_products(session=db, organization_id=fake_org_id)
    assert top == []


def test_get_top_products_limit(db: Session) -> None:
    """Top products should respect the limit parameter."""
    organization_id = _get_default_org_id(db)
    # Create multiple sales to ensure we have products
    create_random_sale(db, organization_id=organization_id, num_items=3)
    top = crud.get_top_products(
        session=db, organization_id=organization_id, limit=2
    )
    assert len(top) <= 2


def test_get_top_products_ordered_by_quantity(db: Session) -> None:
    """Top products should be ordered by quantity sold descending."""
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id, num_items=2)
    top = crud.get_top_products(session=db, organization_id=organization_id)
    if len(top) >= 2:
        assert top[0]["quantity_sold"] >= top[1]["quantity_sold"]


# ---------------------------------------------------------------------------
# get_sales_by_day
# ---------------------------------------------------------------------------


def test_get_sales_by_day(db: Session) -> None:
    """Sales by day should include today's sales."""
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id)
    by_day = crud.get_sales_by_day(session=db, organization_id=organization_id)
    assert isinstance(by_day, list)
    assert len(by_day) >= 1
    item = by_day[-1]  # Most recent day should be last (ordered by date)
    assert "date" in item
    assert "count" in item
    assert "total" in item
    assert item["count"] >= 1
    assert item["total"] > Decimal("0")


def test_get_sales_by_day_empty(db: Session) -> None:
    """Sales by day for an org with no sales should return an empty list."""
    import uuid

    fake_org_id = uuid.uuid4()
    by_day = crud.get_sales_by_day(session=db, organization_id=fake_org_id)
    assert by_day == []


def test_get_sales_by_day_format(db: Session) -> None:
    """Each sales_by_day item should have a valid date string."""
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id)
    by_day = crud.get_sales_by_day(session=db, organization_id=organization_id)
    assert len(by_day) >= 1
    # Verify date format (YYYY-MM-DD)
    from datetime import date

    for item in by_day:
        date.fromisoformat(item["date"])  # Should not raise


# ---------------------------------------------------------------------------
# get_dashboard_stats
# ---------------------------------------------------------------------------


def test_get_dashboard_stats(db: Session) -> None:
    """Dashboard stats should return the full unified structure."""
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id)
    stats = crud.get_dashboard_stats(
        session=db, organization_id=organization_id
    )
    # Verify top-level keys
    assert "sales_today" in stats
    assert "sales_month" in stats
    assert "low_stock_count" in stats
    assert "average_ticket" in stats
    assert "top_products" in stats
    assert "sales_by_day" in stats

    # Verify nested structure
    assert "count" in stats["sales_today"]
    assert "total" in stats["sales_today"]
    assert "count" in stats["sales_month"]
    assert "total" in stats["sales_month"]
    assert stats["sales_today"]["count"] >= 1
    assert stats["sales_month"]["count"] >= 1
    assert isinstance(stats["top_products"], list)
    assert isinstance(stats["sales_by_day"], list)


def test_get_dashboard_stats_low_stock(db: Session) -> None:
    """Dashboard stats should include low stock count."""
    organization_id = _get_default_org_id(db)
    # Create a product with stock at or below minimum
    create_random_product(
        db, organization_id=organization_id, stock_quantity=5, stock_min=10
    )
    stats = crud.get_dashboard_stats(
        session=db, organization_id=organization_id
    )
    assert stats["low_stock_count"] >= 1


def test_get_dashboard_stats_average_ticket(db: Session) -> None:
    """Average ticket should be non-negative when there are sales."""
    organization_id = _get_default_org_id(db)
    create_random_sale(db, organization_id=organization_id)
    stats = crud.get_dashboard_stats(
        session=db, organization_id=organization_id
    )
    assert stats["average_ticket"] >= Decimal("0")

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app import crud
from app.models import UserCreate
from tests.utils.sale import create_random_sale
from tests.utils.user import (
    _get_default_org_id,
    _get_role_id,
    user_authentication_headers,
)
from tests.utils.utils import random_email, random_lower_string


def _create_seller_headers(client: TestClient, db: Session) -> dict[str, str]:
    """Create a seller user and return auth headers."""
    org_id = _get_default_org_id(db)
    role_id = _get_role_id(db, "seller")
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(
        email=email,
        password=password,
        first_name="Seller",
        last_name="User",
        role_id=role_id,
    )
    crud.create_user(session=db, user_create=user_in, organization_id=org_id)
    return user_authentication_headers(client=client, email=email, password=password)


# ---------------------------------------------------------------------------
# GET /dashboard/stats
# ---------------------------------------------------------------------------


def test_read_dashboard_stats(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Admin can read dashboard stats."""
    create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/dashboard/stats",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    # Verify top-level structure
    assert "sales_today" in data
    assert "sales_month" in data
    assert "low_stock_count" in data
    assert "average_ticket" in data
    assert "top_products" in data
    assert "sales_by_day" in data


def test_read_dashboard_stats_sales_today(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Sales today should have count and total."""
    create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/dashboard/stats",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "count" in data["sales_today"]
    assert "total" in data["sales_today"]
    assert data["sales_today"]["count"] >= 1
    assert float(data["sales_today"]["total"]) > 0


def test_read_dashboard_stats_sales_month(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Sales month should have count and total."""
    create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/dashboard/stats",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "count" in data["sales_month"]
    assert "total" in data["sales_month"]
    assert data["sales_month"]["count"] >= 1
    assert float(data["sales_month"]["total"]) > 0


def test_read_dashboard_stats_top_products(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Top products should be a list with product details."""
    create_random_sale(db, num_items=2)
    r = client.get(
        f"{settings.API_V1_STR}/dashboard/stats",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["top_products"], list)
    assert len(data["top_products"]) >= 1
    product = data["top_products"][0]
    assert "product_id" in product
    assert "product_name" in product
    assert "quantity_sold" in product
    assert "revenue" in product
    assert product["quantity_sold"] > 0


def test_read_dashboard_stats_sales_by_day(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Sales by day should be a list with date, count, total."""
    create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/dashboard/stats",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["sales_by_day"], list)
    assert len(data["sales_by_day"]) >= 1
    day = data["sales_by_day"][-1]
    assert "date" in day
    assert "count" in day
    assert "total" in day


def test_read_dashboard_stats_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user (viewer) can view dashboard stats."""
    r = client.get(
        f"{settings.API_V1_STR}/dashboard/stats",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "sales_today" in data
    assert "sales_month" in data
    assert "low_stock_count" in data
    assert "average_ticket" in data
    assert "top_products" in data
    assert "sales_by_day" in data


def test_read_dashboard_stats_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role can view dashboard stats."""
    headers = _create_seller_headers(client, db)
    r = client.get(
        f"{settings.API_V1_STR}/dashboard/stats",
        headers=headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "sales_today" in data


def test_read_dashboard_stats_unauthenticated(
    client: TestClient,
) -> None:
    """Unauthenticated requests should be rejected."""
    r = client.get(f"{settings.API_V1_STR}/dashboard/stats")
    assert r.status_code == 401

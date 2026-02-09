import uuid
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.category import create_random_category
from tests.utils.product import create_random_product
from tests.utils.user import (
    _get_default_org_id,
    _get_role_id,
    user_authentication_headers,
)
from tests.utils.utils import random_email, random_lower_string

from app import crud
from app.models import UserCreate


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
# GET /products/
# ---------------------------------------------------------------------------


def test_read_products(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_product(db)
    create_random_product(db)
    r = client.get(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 2
    assert len(data["data"]) >= 2


def test_read_products_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user can list products."""
    r = client.get(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data


# ---------------------------------------------------------------------------
# POST /products/
# ---------------------------------------------------------------------------


def test_create_product(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    sku = f"SKU-{random_lower_string()[:16]}"
    r = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json={
            "name": "Test Product",
            "sku": sku,
            "description": "A test product",
            "cost_price": "10.00",
            "sale_price": "25.50",
            "stock_quantity": 100,
            "stock_min": 10,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Test Product"
    assert data["sku"] == sku
    assert data["is_active"] is True
    assert data["category_id"] is None


def test_create_product_with_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    category = create_random_category(db)
    sku = f"SKU-{random_lower_string()[:16]}"
    r = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json={
            "name": "Categorized Product",
            "sku": sku,
            "category_id": str(category.id),
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["category_id"] == str(category.id)


def test_create_product_invalid_category(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    sku = f"SKU-{random_lower_string()[:16]}"
    r = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json={
            "name": "Bad Category",
            "sku": sku,
            "category_id": str(uuid.uuid4()),
        },
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Category not found"


def test_create_product_duplicate_sku(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    r = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json={"name": "Duplicate SKU", "sku": product.sku},
    )
    assert r.status_code == 409
    assert "SKU already exists" in r.json()["detail"]


def test_create_product_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role can create products."""
    headers = _create_seller_headers(client, db)
    sku = f"SKU-{random_lower_string()[:16]}"
    r = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=headers,
        json={"name": "Seller Product", "sku": sku},
    )
    assert r.status_code == 200


def test_create_product_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Viewer role cannot create products."""
    r = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json={"name": "Forbidden", "sku": "SKU-FORBIDDEN"},
    )
    assert r.status_code == 403


def test_create_product_negative_price(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Negative prices should be rejected."""
    r = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json={
            "name": "Negative Price",
            "sku": f"SKU-{random_lower_string()[:16]}",
            "cost_price": "-5.00",
        },
    )
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# GET /products/low-stock
# ---------------------------------------------------------------------------


def test_read_low_stock_products(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # Create a low-stock product
    create_random_product(db, stock_quantity=2, stock_min=10)
    r = client.get(
        f"{settings.API_V1_STR}/products/low-stock",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 1
    for item in data["data"]:
        assert item["stock_quantity"] <= item["stock_min"]


# ---------------------------------------------------------------------------
# GET /products/{id}
# ---------------------------------------------------------------------------


def test_read_product_by_id(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    r = client.get(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == str(product.id)
    assert data["name"] == product.name
    assert data["sku"] == product.sku


def test_read_product_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/products/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /products/{id}
# ---------------------------------------------------------------------------


def test_update_product(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    new_name = f"Updated-{random_lower_string()[:16]}"
    r = client.patch(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=superuser_token_headers,
        json={"name": new_name, "description": "Updated description"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == new_name
    assert data["description"] == "Updated description"


def test_update_product_sku(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    new_sku = f"SKU-{random_lower_string()[:16]}"
    r = client.patch(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=superuser_token_headers,
        json={"sku": new_sku},
    )
    assert r.status_code == 200
    assert r.json()["sku"] == new_sku


def test_update_product_duplicate_sku(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product1 = create_random_product(db)
    product2 = create_random_product(db)
    r = client.patch(
        f"{settings.API_V1_STR}/products/{product2.id}",
        headers=superuser_token_headers,
        json={"sku": product1.sku},
    )
    assert r.status_code == 409
    assert "SKU already exists" in r.json()["detail"]


def test_update_product_invalid_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    r = client.patch(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=superuser_token_headers,
        json={"category_id": str(uuid.uuid4())},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Category not found"


def test_update_product_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.patch(
        f"{settings.API_V1_STR}/products/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json={"name": "Ghost"},
    )
    assert r.status_code == 404


def test_update_product_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    r = client.patch(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=normal_user_token_headers,
        json={"name": "Forbidden"},
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# DELETE /products/{id}
# ---------------------------------------------------------------------------


def test_delete_product(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    r = client.delete(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Product deleted successfully"

    # Verify it's soft-deleted (not visible via API)
    r2 = client.get(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=superuser_token_headers,
    )
    assert r2.status_code == 404


def test_delete_product_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/products/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


def test_delete_product_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    r = client.delete(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403


def test_delete_product_forbidden_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role cannot delete products."""
    headers = _create_seller_headers(client, db)
    product = create_random_product(db)
    r = client.delete(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=headers,
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# POST /products/{id}/adjust-stock
# ---------------------------------------------------------------------------


def test_adjust_stock_add(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/products/{product.id}/adjust-stock",
        headers=superuser_token_headers,
        json={"quantity": 20, "reason": "Restocking"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["stock_quantity"] == 70


def test_adjust_stock_subtract(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/products/{product.id}/adjust-stock",
        headers=superuser_token_headers,
        json={"quantity": -10, "reason": "Damaged goods"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["stock_quantity"] == 40


def test_adjust_stock_negative_result(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Cannot reduce stock below zero."""
    product = create_random_product(db, stock_quantity=5)
    r = client.post(
        f"{settings.API_V1_STR}/products/{product.id}/adjust-stock",
        headers=superuser_token_headers,
        json={"quantity": -10, "reason": "Too many removed"},
    )
    assert r.status_code == 400
    assert "cannot be negative" in r.json()["detail"]


def test_adjust_stock_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/products/{uuid.uuid4()}/adjust-stock",
        headers=superuser_token_headers,
        json={"quantity": 10, "reason": "Test"},
    )
    assert r.status_code == 404


def test_adjust_stock_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role can adjust stock."""
    headers = _create_seller_headers(client, db)
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/products/{product.id}/adjust-stock",
        headers=headers,
        json={"quantity": 10, "reason": "Seller restock"},
    )
    assert r.status_code == 200
    assert r.json()["stock_quantity"] == 60


def test_adjust_stock_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db)
    r = client.post(
        f"{settings.API_V1_STR}/products/{product.id}/adjust-stock",
        headers=normal_user_token_headers,
        json={"quantity": 10, "reason": "Forbidden"},
    )
    assert r.status_code == 403

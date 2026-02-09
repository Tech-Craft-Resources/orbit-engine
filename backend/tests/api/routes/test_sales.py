import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app import crud
from app.models import UserCreate
from tests.utils.customer import create_random_customer
from tests.utils.product import create_random_product
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
# GET /sales/
# ---------------------------------------------------------------------------


def test_read_sales(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 1


def test_read_sales_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user can list sales."""
    r = client.get(
        f"{settings.API_V1_STR}/sales/",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data


# ---------------------------------------------------------------------------
# POST /sales/
# ---------------------------------------------------------------------------


def test_create_sale(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=50)
    customer = create_random_customer(db)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "customer_id": str(customer.id),
            "payment_method": "cash",
            "discount": "0.00",
            "tax": "0.00",
            "notes": "Test sale via API",
            "items": [
                {"product_id": str(product.id), "quantity": 2},
            ],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "completed"
    assert data["customer_id"] == str(customer.id)
    assert data["payment_method"] == "cash"
    assert data["notes"] == "Test sale via API"
    assert data["invoice_number"].startswith("INV-")
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == str(product.id)
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["product_name"] == product.name
    assert data["items"][0]["product_sku"] == product.sku
    # Verify subtotal calculation
    expected_subtotal = float(product.sale_price) * 2
    assert float(data["subtotal"]) == expected_subtotal
    assert float(data["total"]) == expected_subtotal


def test_create_sale_without_customer(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "payment_method": "card",
            "items": [
                {"product_id": str(product.id), "quantity": 1},
            ],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["customer_id"] is None
    assert data["payment_method"] == "card"


def test_create_sale_multiple_items(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product1 = create_random_product(db, stock_quantity=50)
    product2 = create_random_product(db, stock_quantity=30)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "payment_method": "transfer",
            "items": [
                {"product_id": str(product1.id), "quantity": 3},
                {"product_id": str(product2.id), "quantity": 1},
            ],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) == 2
    expected_subtotal = float(product1.sale_price) * 3 + float(product2.sale_price) * 1
    assert float(data["subtotal"]) == expected_subtotal


def test_create_sale_with_discount_and_tax(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "payment_method": "cash",
            "discount": "5.00",
            "tax": "10.00",
            "items": [
                {"product_id": str(product.id), "quantity": 2},
            ],
        },
    )
    assert r.status_code == 200
    data = r.json()
    subtotal = float(data["subtotal"])
    expected_total = subtotal - 5.00 + 10.00
    assert float(data["total"]) == expected_total
    assert float(data["discount"]) == 5.00
    assert float(data["tax"]) == 10.00


def test_create_sale_insufficient_stock(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=3)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 10},
            ],
        },
    )
    assert r.status_code == 400
    assert "Insufficient stock" in r.json()["detail"]


def test_create_sale_product_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [
                {"product_id": str(uuid.uuid4()), "quantity": 1},
            ],
        },
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"]


def test_create_sale_inactive_product(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=50)
    crud.soft_delete_product(session=db, db_product=product)
    # The product is now soft-deleted, get_product_by_id filters deleted_at
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 1},
            ],
        },
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"]


def test_create_sale_customer_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "customer_id": str(uuid.uuid4()),
            "items": [
                {"product_id": str(product.id), "quantity": 1},
            ],
        },
    )
    assert r.status_code == 404
    assert "Customer not found" in r.json()["detail"]


def test_create_sale_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role can create sales."""
    headers = _create_seller_headers(client, db)
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 1},
            ],
        },
    )
    assert r.status_code == 200


def test_create_sale_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Viewer role cannot create sales."""
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=normal_user_token_headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 1},
            ],
        },
    )
    assert r.status_code == 403


def test_create_sale_empty_items(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """A sale must have at least one item."""
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [],
        },
    )
    assert r.status_code == 422


def test_create_sale_zero_quantity(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Quantity must be greater than zero."""
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 0},
            ],
        },
    )
    assert r.status_code == 422


def test_create_sale_deducts_stock(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Creating a sale should deduct stock from products."""
    product = create_random_product(db, stock_quantity=50)
    initial_stock = product.stock_quantity

    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 5},
            ],
        },
    )
    assert r.status_code == 200

    # Verify stock was deducted
    org_id = _get_default_org_id(db)
    db.expire_all()
    updated_product = crud.get_product_by_id(
        session=db, product_id=product.id, organization_id=org_id
    )
    assert updated_product is not None
    assert updated_product.stock_quantity == initial_stock - 5


def test_create_sale_creates_inventory_movements(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Creating a sale should create inventory movement records."""
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 3},
            ],
        },
    )
    assert r.status_code == 200
    sale_data = r.json()

    # Check inventory movements for this product
    r2 = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/movements",
        headers=superuser_token_headers,
    )
    assert r2.status_code == 200
    movements = r2.json()
    # Find the sale movement
    found = False
    for m in movements["data"]:
        if (
            m["movement_type"] == "sale"
            and m["reference_id"] == sale_data["id"]
        ):
            assert m["quantity"] == -3
            found = True
            break
    assert found, "Sale inventory movement not found"


def test_create_sale_updates_customer_stats(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Creating a sale with a customer should update their purchase stats."""
    customer = create_random_customer(db)
    product = create_random_product(db, stock_quantity=50)

    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "customer_id": str(customer.id),
            "items": [
                {"product_id": str(product.id), "quantity": 2},
            ],
        },
    )
    assert r.status_code == 200
    sale_data = r.json()

    # Verify customer stats were updated
    db.expire_all()
    org_id = _get_default_org_id(db)
    updated_customer = crud.get_customer_by_id(
        session=db, customer_id=customer.id, organization_id=org_id
    )
    assert updated_customer is not None
    assert updated_customer.purchases_count >= 1
    assert float(updated_customer.total_purchases) >= float(sale_data["total"])


# ---------------------------------------------------------------------------
# GET /sales/today
# ---------------------------------------------------------------------------


def test_read_sales_today(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/sales/today",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 1


def test_read_sales_today_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user can view today's sales."""
    r = client.get(
        f"{settings.API_V1_STR}/sales/today",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200


# ---------------------------------------------------------------------------
# GET /sales/stats
# ---------------------------------------------------------------------------


def test_read_sales_stats(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/sales/stats",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "sales_today_count" in data
    assert "sales_today_total" in data
    assert "sales_month_count" in data
    assert "sales_month_total" in data
    assert "average_ticket" in data
    assert data["sales_today_count"] >= 1


def test_read_sales_stats_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user can view sales stats."""
    r = client.get(
        f"{settings.API_V1_STR}/sales/stats",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200


# ---------------------------------------------------------------------------
# GET /sales/{id}
# ---------------------------------------------------------------------------


def test_read_sale_by_id(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    sale = create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/sales/{sale.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == str(sale.id)
    assert data["invoice_number"] == sale.invoice_number
    assert "items" in data
    assert len(data["items"]) >= 1


def test_read_sale_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/sales/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


def test_read_sale_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Any authenticated user can view a sale."""
    sale = create_random_sale(db)
    r = client.get(
        f"{settings.API_V1_STR}/sales/{sale.id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200


# ---------------------------------------------------------------------------
# POST /sales/{id}/cancel
# ---------------------------------------------------------------------------


def test_cancel_sale(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    sale = create_random_sale(db)
    r = client.post(
        f"{settings.API_V1_STR}/sales/{sale.id}/cancel",
        headers=superuser_token_headers,
        json={"reason": "Customer requested refund"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "cancelled"
    assert data["cancellation_reason"] == "Customer requested refund"
    assert data["cancelled_at"] is not None
    assert data["cancelled_by"] is not None


def test_cancel_sale_already_cancelled(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    sale = create_random_sale(db)
    # Cancel it once
    r1 = client.post(
        f"{settings.API_V1_STR}/sales/{sale.id}/cancel",
        headers=superuser_token_headers,
        json={"reason": "First cancel"},
    )
    assert r1.status_code == 200
    # Try to cancel again
    r2 = client.post(
        f"{settings.API_V1_STR}/sales/{sale.id}/cancel",
        headers=superuser_token_headers,
        json={"reason": "Second cancel"},
    )
    assert r2.status_code == 400
    assert "already cancelled" in r2.json()["detail"]


def test_cancel_sale_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/sales/{uuid.uuid4()}/cancel",
        headers=superuser_token_headers,
        json={"reason": "Not found"},
    )
    assert r.status_code == 404


def test_cancel_sale_restores_stock(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Cancelling a sale should restore stock for all items."""
    product = create_random_product(db, stock_quantity=50)
    initial_stock = product.stock_quantity

    # Create a sale
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 5},
            ],
        },
    )
    assert r.status_code == 200
    sale_id = r.json()["id"]

    # Verify stock was deducted
    org_id = _get_default_org_id(db)
    db.expire_all()
    updated_product = crud.get_product_by_id(
        session=db, product_id=product.id, organization_id=org_id
    )
    assert updated_product is not None
    assert updated_product.stock_quantity == initial_stock - 5

    # Cancel the sale
    r2 = client.post(
        f"{settings.API_V1_STR}/sales/{sale_id}/cancel",
        headers=superuser_token_headers,
        json={"reason": "Test cancellation"},
    )
    assert r2.status_code == 200

    # Verify stock was restored
    db.expire_all()
    restored_product = crud.get_product_by_id(
        session=db, product_id=product.id, organization_id=org_id
    )
    assert restored_product is not None
    assert restored_product.stock_quantity == initial_stock


def test_cancel_sale_reverts_customer_stats(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Cancelling a sale should revert customer purchase stats."""
    customer = create_random_customer(db)
    product = create_random_product(db, stock_quantity=50)

    # Create a sale with customer
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "customer_id": str(customer.id),
            "items": [
                {"product_id": str(product.id), "quantity": 2},
            ],
        },
    )
    assert r.status_code == 200
    sale_id = r.json()["id"]

    # Record stats after sale
    org_id = _get_default_org_id(db)
    db.expire_all()
    customer_after_sale = crud.get_customer_by_id(
        session=db, customer_id=customer.id, organization_id=org_id
    )
    assert customer_after_sale is not None
    count_after_sale = customer_after_sale.purchases_count

    # Cancel the sale
    r2 = client.post(
        f"{settings.API_V1_STR}/sales/{sale_id}/cancel",
        headers=superuser_token_headers,
        json={"reason": "Revert test"},
    )
    assert r2.status_code == 200

    # Verify stats were reverted
    db.expire_all()
    customer_after_cancel = crud.get_customer_by_id(
        session=db, customer_id=customer.id, organization_id=org_id
    )
    assert customer_after_cancel is not None
    assert customer_after_cancel.purchases_count == count_after_sale - 1


def test_cancel_sale_creates_return_movements(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Cancelling a sale should create return inventory movements."""
    product = create_random_product(db, stock_quantity=50)

    # Create a sale
    r = client.post(
        f"{settings.API_V1_STR}/sales/",
        headers=superuser_token_headers,
        json={
            "items": [
                {"product_id": str(product.id), "quantity": 3},
            ],
        },
    )
    assert r.status_code == 200
    sale_id = r.json()["id"]

    # Cancel the sale
    r2 = client.post(
        f"{settings.API_V1_STR}/sales/{sale_id}/cancel",
        headers=superuser_token_headers,
        json={"reason": "Return movement test"},
    )
    assert r2.status_code == 200

    # Check for return movements
    r3 = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/movements",
        headers=superuser_token_headers,
    )
    assert r3.status_code == 200
    movements = r3.json()
    found_return = False
    for m in movements["data"]:
        if m["movement_type"] == "return" and m["reference_id"] == sale_id:
            assert m["quantity"] == 3
            found_return = True
            break
    assert found_return, "Return inventory movement not found"


def test_cancel_sale_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role can cancel sales."""
    headers = _create_seller_headers(client, db)
    sale = create_random_sale(db)
    r = client.post(
        f"{settings.API_V1_STR}/sales/{sale.id}/cancel",
        headers=headers,
        json={"reason": "Seller cancellation"},
    )
    assert r.status_code == 200


def test_cancel_sale_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Viewer role cannot cancel sales."""
    sale = create_random_sale(db)
    r = client.post(
        f"{settings.API_V1_STR}/sales/{sale.id}/cancel",
        headers=normal_user_token_headers,
        json={"reason": "Forbidden cancel"},
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# GET /customers/{id}/sales
# ---------------------------------------------------------------------------


def test_read_customer_sales(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    create_random_sale(db, customer_id=customer.id)
    create_random_sale(db, customer_id=customer.id)
    r = client.get(
        f"{settings.API_V1_STR}/customers/{customer.id}/sales",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 2


def test_read_customer_sales_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/customers/{uuid.uuid4()}/sales",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


def test_read_customer_sales_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Any authenticated user can view customer sales."""
    customer = create_random_customer(db)
    r = client.get(
        f"{settings.API_V1_STR}/customers/{customer.id}/sales",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200

import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app import crud
from app.models import UserCreate
from tests.utils.inventory_movement import create_random_movement
from tests.utils.product import create_random_product
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
# GET /inventory-movements/
# ---------------------------------------------------------------------------


def test_read_movements(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_movement(db)
    r = client.get(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 1


def test_read_movements_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user can list movements."""
    r = client.get(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data


# ---------------------------------------------------------------------------
# POST /inventory-movements/
# ---------------------------------------------------------------------------


def test_create_movement_purchase(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=superuser_token_headers,
        json={
            "product_id": str(product.id),
            "movement_type": "purchase",
            "quantity": 20,
            "reason": "Restocking from supplier",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["movement_type"] == "purchase"
    assert data["quantity"] == 20
    assert data["previous_stock"] == 50
    assert data["new_stock"] == 70
    assert data["reason"] == "Restocking from supplier"


def test_create_movement_adjustment(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=30)
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=superuser_token_headers,
        json={
            "product_id": str(product.id),
            "movement_type": "adjustment",
            "quantity": -5,
            "reason": "Damaged goods",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["movement_type"] == "adjustment"
    assert data["quantity"] == -5
    assert data["previous_stock"] == 30
    assert data["new_stock"] == 25


def test_create_movement_return(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=40)
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=superuser_token_headers,
        json={
            "product_id": str(product.id),
            "movement_type": "return",
            "quantity": 3,
            "reason": "Customer return",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["movement_type"] == "return"
    assert data["quantity"] == 3
    assert data["previous_stock"] == 40
    assert data["new_stock"] == 43


def test_create_movement_invalid_type_sale(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Cannot create 'sale' type movements directly."""
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=superuser_token_headers,
        json={
            "product_id": str(product.id),
            "movement_type": "sale",
            "quantity": -5,
        },
    )
    assert r.status_code == 400
    assert "Invalid movement type" in r.json()["detail"]


def test_create_movement_invalid_type_unknown(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Unknown movement types should be rejected."""
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=superuser_token_headers,
        json={
            "product_id": str(product.id),
            "movement_type": "theft",
            "quantity": -5,
        },
    )
    assert r.status_code == 400
    assert "Invalid movement type" in r.json()["detail"]


def test_create_movement_product_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=superuser_token_headers,
        json={
            "product_id": str(uuid.uuid4()),
            "movement_type": "purchase",
            "quantity": 10,
        },
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Product not found"


def test_create_movement_negative_stock(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Cannot create a movement that would result in negative stock."""
    product = create_random_product(db, stock_quantity=5)
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=superuser_token_headers,
        json={
            "product_id": str(product.id),
            "movement_type": "adjustment",
            "quantity": -10,
            "reason": "Too many removed",
        },
    )
    assert r.status_code == 400
    assert "cannot be negative" in r.json()["detail"]


def test_create_movement_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role can create movements."""
    headers = _create_seller_headers(client, db)
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=headers,
        json={
            "product_id": str(product.id),
            "movement_type": "purchase",
            "quantity": 10,
            "reason": "Seller restock",
        },
    )
    assert r.status_code == 200


def test_create_movement_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Viewer role cannot create movements."""
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/inventory-movements/",
        headers=normal_user_token_headers,
        json={
            "product_id": str(product.id),
            "movement_type": "purchase",
            "quantity": 10,
        },
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# GET /inventory-movements/{id}
# ---------------------------------------------------------------------------


def test_read_movement_by_id(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    movement = create_random_movement(db)
    r = client.get(
        f"{settings.API_V1_STR}/inventory-movements/{movement.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == str(movement.id)
    assert data["movement_type"] == movement.movement_type


def test_read_movement_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/inventory-movements/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# GET /products/{id}/movements
# ---------------------------------------------------------------------------


def test_read_product_movements(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, stock_quantity=100)
    # Create some movements for this product
    create_random_movement(db, product_id=product.id, quantity=10)
    create_random_movement(db, product_id=product.id, quantity=-5)

    r = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/movements",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 2


def test_read_product_movements_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/products/{uuid.uuid4()}/movements",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


def test_read_product_movements_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Any authenticated user can view product movements."""
    product = create_random_product(db, stock_quantity=100)
    r = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/movements",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200


# ---------------------------------------------------------------------------
# POST /products/{id}/adjust-stock (now creates movement)
# ---------------------------------------------------------------------------


def test_adjust_stock_creates_movement(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Adjusting stock should also create an inventory movement record."""
    product = create_random_product(db, stock_quantity=50)
    r = client.post(
        f"{settings.API_V1_STR}/products/{product.id}/adjust-stock",
        headers=superuser_token_headers,
        json={"quantity": 20, "reason": "Restocking"},
    )
    assert r.status_code == 200
    assert r.json()["stock_quantity"] == 70

    # Verify movement was created
    r2 = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/movements",
        headers=superuser_token_headers,
    )
    assert r2.status_code == 200
    movements = r2.json()
    assert movements["count"] >= 1
    # Find the adjustment movement
    found = False
    for m in movements["data"]:
        if m["movement_type"] == "adjustment" and m["quantity"] == 20:
            assert m["previous_stock"] == 50
            assert m["new_stock"] == 70
            assert m["reason"] == "Restocking"
            found = True
            break
    assert found, "Adjustment movement not found"

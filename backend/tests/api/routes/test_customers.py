import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.customer import create_random_customer
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
# GET /customers/
# ---------------------------------------------------------------------------


def test_read_customers(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_customer(db)
    create_random_customer(db)
    r = client.get(
        f"{settings.API_V1_STR}/customers/",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 2
    assert len(data["data"]) >= 2


def test_read_customers_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user can list customers."""
    r = client.get(
        f"{settings.API_V1_STR}/customers/",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data


# ---------------------------------------------------------------------------
# POST /customers/
# ---------------------------------------------------------------------------


def test_create_customer(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    doc_number = f"DOC-{random_lower_string()[:16]}"
    r = client.post(
        f"{settings.API_V1_STR}/customers/",
        headers=superuser_token_headers,
        json={
            "document_type": "DNI",
            "document_number": doc_number,
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan@example.com",
            "phone": "555-0100",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["document_number"] == doc_number
    assert data["first_name"] == "Juan"
    assert data["is_active"] is True
    assert data["total_purchases"] == "0.00"
    assert data["purchases_count"] == 0


def test_create_customer_duplicate_document(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    r = client.post(
        f"{settings.API_V1_STR}/customers/",
        headers=superuser_token_headers,
        json={
            "document_type": "DNI",
            "document_number": customer.document_number,
            "first_name": "Duplicate",
            "last_name": "Customer",
        },
    )
    assert r.status_code == 409
    assert "document number already exists" in r.json()["detail"]


def test_create_customer_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role can create customers."""
    headers = _create_seller_headers(client, db)
    doc_number = f"DOC-{random_lower_string()[:16]}"
    r = client.post(
        f"{settings.API_V1_STR}/customers/",
        headers=headers,
        json={
            "document_type": "RUC",
            "document_number": doc_number,
            "first_name": "Seller",
            "last_name": "Created",
        },
    )
    assert r.status_code == 200


def test_create_customer_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Viewer role cannot create customers."""
    r = client.post(
        f"{settings.API_V1_STR}/customers/",
        headers=normal_user_token_headers,
        json={
            "document_type": "DNI",
            "document_number": "FORBIDDEN-001",
            "first_name": "Forbidden",
            "last_name": "Customer",
        },
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# GET /customers/{id}
# ---------------------------------------------------------------------------


def test_read_customer_by_id(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    r = client.get(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == str(customer.id)
    assert data["document_number"] == customer.document_number


def test_read_customer_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/customers/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /customers/{id}
# ---------------------------------------------------------------------------


def test_update_customer(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    r = client.patch(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=superuser_token_headers,
        json={"first_name": "Updated", "last_name": "Name"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"


def test_update_customer_document_number(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    new_doc = f"DOC-{random_lower_string()[:16]}"
    r = client.patch(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=superuser_token_headers,
        json={"document_number": new_doc},
    )
    assert r.status_code == 200
    assert r.json()["document_number"] == new_doc


def test_update_customer_duplicate_document(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    customer1 = create_random_customer(db)
    customer2 = create_random_customer(db)
    r = client.patch(
        f"{settings.API_V1_STR}/customers/{customer2.id}",
        headers=superuser_token_headers,
        json={"document_number": customer1.document_number},
    )
    assert r.status_code == 409
    assert "document number already exists" in r.json()["detail"]


def test_update_customer_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.patch(
        f"{settings.API_V1_STR}/customers/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json={"first_name": "Ghost"},
    )
    assert r.status_code == 404


def test_update_customer_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    r = client.patch(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=normal_user_token_headers,
        json={"first_name": "Forbidden"},
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# DELETE /customers/{id}
# ---------------------------------------------------------------------------


def test_delete_customer(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    r = client.delete(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Customer deleted successfully"

    # Verify it's soft-deleted (not visible via API)
    r2 = client.get(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=superuser_token_headers,
    )
    assert r2.status_code == 404


def test_delete_customer_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/customers/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


def test_delete_customer_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    r = client.delete(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403


def test_delete_customer_forbidden_seller(
    client: TestClient, db: Session
) -> None:
    """Seller role cannot delete customers."""
    headers = _create_seller_headers(client, db)
    customer = create_random_customer(db)
    r = client.delete(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=headers,
    )
    assert r.status_code == 403

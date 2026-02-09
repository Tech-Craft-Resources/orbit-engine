import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.category import create_random_category
from tests.utils.utils import random_lower_string


# ---------------------------------------------------------------------------
# GET /categories/
# ---------------------------------------------------------------------------


def test_read_categories(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_category(db)
    create_random_category(db)
    r = client.get(
        f"{settings.API_V1_STR}/categories/",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 2
    assert len(data["data"]) >= 2


def test_read_categories_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user can list categories."""
    r = client.get(
        f"{settings.API_V1_STR}/categories/",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data


# ---------------------------------------------------------------------------
# POST /categories/
# ---------------------------------------------------------------------------


def test_create_category(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    name = f"Cat-{random_lower_string()[:16]}"
    r = client.post(
        f"{settings.API_V1_STR}/categories/",
        headers=superuser_token_headers,
        json={"name": name, "description": "A test category"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == name
    assert data["description"] == "A test category"
    assert data["is_active"] is True
    assert data["parent_id"] is None


def test_create_category_with_parent(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    parent = create_random_category(db)
    child_name = f"Child-{random_lower_string()[:16]}"
    r = client.post(
        f"{settings.API_V1_STR}/categories/",
        headers=superuser_token_headers,
        json={"name": child_name, "parent_id": str(parent.id)},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == child_name
    assert data["parent_id"] == str(parent.id)


def test_create_category_invalid_parent(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/categories/",
        headers=superuser_token_headers,
        json={"name": "Orphan", "parent_id": str(uuid.uuid4())},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Parent category not found"


def test_create_category_duplicate_name(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    category = create_random_category(db)
    r = client.post(
        f"{settings.API_V1_STR}/categories/",
        headers=superuser_token_headers,
        json={"name": category.name},
    )
    assert r.status_code == 409
    assert "already exists" in r.json()["detail"]


def test_create_category_same_name_different_parent(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Same name is allowed under different parents."""
    parent1 = create_random_category(db)
    parent2 = create_random_category(db)
    name = f"Sub-{random_lower_string()[:16]}"

    r1 = client.post(
        f"{settings.API_V1_STR}/categories/",
        headers=superuser_token_headers,
        json={"name": name, "parent_id": str(parent1.id)},
    )
    assert r1.status_code == 200

    r2 = client.post(
        f"{settings.API_V1_STR}/categories/",
        headers=superuser_token_headers,
        json={"name": name, "parent_id": str(parent2.id)},
    )
    assert r2.status_code == 200


def test_create_category_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Viewer role cannot create categories."""
    r = client.post(
        f"{settings.API_V1_STR}/categories/",
        headers=normal_user_token_headers,
        json={"name": "Forbidden"},
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# GET /categories/{id}
# ---------------------------------------------------------------------------


def test_read_category_by_id(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    category = create_random_category(db)
    r = client.get(
        f"{settings.API_V1_STR}/categories/{category.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == str(category.id)
    assert data["name"] == category.name


def test_read_category_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/categories/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /categories/{id}
# ---------------------------------------------------------------------------


def test_update_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    category = create_random_category(db)
    new_name = f"Updated-{random_lower_string()[:16]}"
    r = client.patch(
        f"{settings.API_V1_STR}/categories/{category.id}",
        headers=superuser_token_headers,
        json={"name": new_name, "description": "Updated description"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == new_name
    assert data["description"] == "Updated description"


def test_update_category_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.patch(
        f"{settings.API_V1_STR}/categories/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json={"name": "Ghost"},
    )
    assert r.status_code == 404


def test_update_category_self_parent(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    category = create_random_category(db)
    r = client.patch(
        f"{settings.API_V1_STR}/categories/{category.id}",
        headers=superuser_token_headers,
        json={"parent_id": str(category.id)},
    )
    assert r.status_code == 400
    assert "own parent" in r.json()["detail"]


def test_update_category_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    category = create_random_category(db)
    r = client.patch(
        f"{settings.API_V1_STR}/categories/{category.id}",
        headers=normal_user_token_headers,
        json={"name": "Forbidden"},
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# DELETE /categories/{id}
# ---------------------------------------------------------------------------


def test_delete_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    category = create_random_category(db)
    r = client.delete(
        f"{settings.API_V1_STR}/categories/{category.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Category deleted successfully"

    # Verify it's soft-deleted (not visible via API)
    r2 = client.get(
        f"{settings.API_V1_STR}/categories/{category.id}",
        headers=superuser_token_headers,
    )
    assert r2.status_code == 404


def test_delete_category_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/categories/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


def test_delete_category_forbidden_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    category = create_random_category(db)
    r = client.delete(
        f"{settings.API_V1_STR}/categories/{category.id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403

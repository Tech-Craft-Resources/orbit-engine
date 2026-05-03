from fastapi.testclient import TestClient

from app.core.config import settings
from tests.utils.utils import random_email, random_lower_string


def _signup_payload(**overrides: object) -> dict:
    """Build a valid OrganizationSignup payload with random data."""
    base: dict = {
        "organization_name": f"Org {random_lower_string()[:16]}",
        "organization_slug": f"org-{random_lower_string()[:12]}",
        "admin_email": random_email(),
        "admin_password": random_lower_string()[:16],
        "admin_first_name": "Admin",
        "admin_last_name": "Test",
    }
    base.update(overrides)
    return base


def _signup(client: TestClient, **overrides: object) -> dict:
    """Create a new org via signup and return the response JSON."""
    r = client.post(
        f"{settings.API_V1_STR}/organizations/signup",
        json=_signup_payload(**overrides),
    )
    assert r.status_code == 201, r.text
    return r.json()


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# POST /organizations/signup
# ---------------------------------------------------------------------------


def test_signup_organization_returns_token_and_user(client: TestClient) -> None:
    payload = _signup_payload()
    r = client.post(f"{settings.API_V1_STR}/organizations/signup", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    user = body["user"]
    assert user["email"] == payload["admin_email"]
    assert user["organization"]["slug"] == payload["organization_slug"]
    assert user["organization"]["name"] == payload["organization_name"]
    assert user["role"]["name"] == "admin"


def test_signup_organization_with_description(client: TestClient) -> None:
    desc = "A detailed description for this org"
    body = _signup(client, organization_description=desc)
    assert body["user"]["organization"]["description"] == desc


def test_signup_organization_duplicate_slug_returns_409(client: TestClient) -> None:
    payload = _signup_payload()
    _signup(client, **{k: v for k, v in payload.items()})
    r = client.post(
        f"{settings.API_V1_STR}/organizations/signup",
        json={**payload, "admin_email": random_email()},
    )
    assert r.status_code == 409
    assert "slug" in r.json()["detail"].lower()


def test_signup_organization_duplicate_email_returns_409(client: TestClient) -> None:
    payload = _signup_payload()
    _signup(client, **{k: v for k, v in payload.items()})
    r = client.post(
        f"{settings.API_V1_STR}/organizations/signup",
        json={**payload, "organization_slug": f"org-{random_lower_string()[:12]}"},
    )
    assert r.status_code == 409
    assert "email" in r.json()["detail"].lower()


def test_signup_organization_invalid_slug_format_returns_422(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/organizations/signup",
        json=_signup_payload(organization_slug="INVALID SLUG!"),
    )
    assert r.status_code == 422


def test_signup_organization_short_password_returns_422(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/organizations/signup",
        json=_signup_payload(admin_password="short"),
    )
    assert r.status_code == 422


def test_signup_organization_missing_required_fields_returns_422(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/organizations/signup",
        json={"organization_name": "Only name"},
    )
    assert r.status_code == 422


def test_signup_organization_slug_too_short_returns_422(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/organizations/signup",
        json=_signup_payload(organization_slug="ab"),
    )
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# GET /organizations/me
# ---------------------------------------------------------------------------


def test_get_my_organization_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/organizations/me", headers=superuser_token_headers
    )
    assert r.status_code == 200
    data = r.json()
    assert "id" in data
    assert "name" in data
    assert "slug" in data
    assert data["is_active"] is True


def test_get_my_organization_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/organizations/me", headers=normal_user_token_headers
    )
    assert r.status_code == 200
    data = r.json()
    assert "id" in data
    assert "slug" in data


def test_get_my_organization_returns_correct_fields(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/organizations/me", headers=superuser_token_headers
    )
    assert r.status_code == 200
    data = r.json()
    for field in ("id", "name", "slug", "is_active", "created_at", "updated_at"):
        assert field in data, f"Missing field: {field}"


def test_get_my_organization_unauthenticated(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/organizations/me")
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# PATCH /organizations/me
# ---------------------------------------------------------------------------


def test_update_organization_name_as_admin(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    new_name = f"Updated {random_lower_string()[:10]}"
    r = client.patch(
        f"{settings.API_V1_STR}/organizations/me",
        headers=superuser_token_headers,
        json={"name": new_name},
    )
    assert r.status_code == 200
    assert r.json()["name"] == new_name


def test_update_organization_description_as_admin(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    new_desc = "Updated description via test"
    r = client.patch(
        f"{settings.API_V1_STR}/organizations/me",
        headers=superuser_token_headers,
        json={"description": new_desc},
    )
    assert r.status_code == 200
    assert r.json()["description"] == new_desc


def test_update_organization_slug_as_admin(client: TestClient) -> None:
    # Use a fresh org so we don't affect the shared "default" org slug
    body = _signup(client)
    token = body["access_token"]
    new_slug = f"upd-{random_lower_string()[:12]}"
    r = client.patch(
        f"{settings.API_V1_STR}/organizations/me",
        headers=_auth_headers(token),
        json={"slug": new_slug},
    )
    assert r.status_code == 200
    assert r.json()["slug"] == new_slug


def test_update_organization_slug_duplicate_returns_409(client: TestClient) -> None:
    body1 = _signup(client)
    body2 = _signup(client)
    slug2 = body2["user"]["organization"]["slug"]
    token1 = body1["access_token"]
    r = client.patch(
        f"{settings.API_V1_STR}/organizations/me",
        headers=_auth_headers(token1),
        json={"slug": slug2},
    )
    assert r.status_code == 409
    assert "slug" in r.json()["detail"].lower()


def test_update_organization_invalid_slug_format_returns_422(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.patch(
        f"{settings.API_V1_STR}/organizations/me",
        headers=superuser_token_headers,
        json={"slug": "INVALID SLUG!"},
    )
    assert r.status_code == 422


def test_update_organization_forbidden_for_viewer(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.patch(
        f"{settings.API_V1_STR}/organizations/me",
        headers=normal_user_token_headers,
        json={"name": "Should fail"},
    )
    assert r.status_code == 403


def test_update_organization_unauthenticated(client: TestClient) -> None:
    r = client.patch(
        f"{settings.API_V1_STR}/organizations/me", json={"name": "No auth"}
    )
    assert r.status_code == 401

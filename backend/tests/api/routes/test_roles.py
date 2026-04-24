from fastapi.testclient import TestClient

from app.core.config import settings

EXPECTED_ROLES = {"admin", "seller", "viewer"}


# ---------------------------------------------------------------------------
# GET /roles/
# ---------------------------------------------------------------------------


def test_list_roles_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/roles/", headers=superuser_token_headers)
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= len(EXPECTED_ROLES)


def test_list_roles_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Any authenticated user can list roles."""
    r = client.get(f"{settings.API_V1_STR}/roles/", headers=normal_user_token_headers)
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "count" in data


def test_list_roles_unauthenticated(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/roles/")
    assert r.status_code == 401


def test_list_roles_contains_expected_roles(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/roles/", headers=superuser_token_headers)
    assert r.status_code == 200
    role_names = {role["name"] for role in r.json()["data"]}
    assert EXPECTED_ROLES.issubset(role_names), (
        f"Missing roles: {EXPECTED_ROLES - role_names}"
    )


def test_list_roles_have_required_fields(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/roles/", headers=superuser_token_headers)
    assert r.status_code == 200
    for role in r.json()["data"]:
        assert "id" in role
        assert "name" in role
        assert "permissions" in role
        assert "created_at" in role
        assert isinstance(role["permissions"], list)


def test_list_roles_count_matches_data_length(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/roles/", headers=superuser_token_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == len(data["data"])

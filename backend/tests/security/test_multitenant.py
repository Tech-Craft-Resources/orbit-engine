"""
Multi-tenant isolation security tests.

Verifies that a user from Organization B cannot read, modify, or delete
any resource that belongs to Organization A — across all domains.

Setup (module-scoped):
  - Org A: admin user + category + product + customer + user
  - Org B: admin user (the attacker)
"""

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from tests.utils.utils import random_email, random_lower_string


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _signup_payload(**overrides: object) -> dict:
    base: dict = {
        "organization_name": f"Org {random_lower_string()[:12]}",
        "organization_slug": f"sec-{random_lower_string()[:10]}",
        "admin_email": random_email(),
        "admin_password": random_lower_string()[:16],
        "admin_first_name": "Admin",
        "admin_last_name": "Test",
    }
    base.update(overrides)
    return base


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _api(path: str) -> str:
    return f"{settings.API_V1_STR}{path}"


# ---------------------------------------------------------------------------
# Module-scoped fixtures: two isolated orgs with data in Org A
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def org_a(client: TestClient) -> dict:
    """Org A — owns all the sensitive data."""
    r = client.post(_api("/organizations/signup"), json=_signup_payload())
    assert r.status_code == 201, r.text
    token = r.json()["access_token"]
    headers = _auth(token)

    # Category
    cat = client.post(
        _api("/categories/"),
        headers=headers,
        json={"name": f"Cat-{random_lower_string()[:8]}", "description": "secret cat"},
    )
    assert cat.status_code == 200, cat.text

    # Product (admin role can create)
    prod = client.post(
        _api("/products/"),
        headers=headers,
        json={
            "name": f"Prod-{random_lower_string()[:8]}",
            "sku": f"SKU-{random_lower_string()[:8]}",
            "sale_price": "9.99",
            "cost_price": "5.00",
        },
    )
    assert prod.status_code == 200, prod.text

    # Customer
    cust = client.post(
        _api("/customers/"),
        headers=headers,
        json={
            "document_type": "DNI",
            "document_number": random_lower_string()[:8],
            "first_name": "Alice",
            "last_name": "OrgA",
        },
    )
    assert cust.status_code == 200, cust.text

    # Second user inside Org A (to test user-list isolation)
    user_r = client.post(
        _api("/users/"),
        headers=headers,
        json={
            "email": random_email(),
            "password": random_lower_string()[:16],
            "first_name": "Inner",
            "last_name": "UserA",
            "role_id": 3,  # viewer
        },
    )
    assert user_r.status_code == 200, user_r.text

    return {
        "headers": headers,
        "category_id": cat.json()["id"],
        "product_id": prod.json()["id"],
        "customer_id": cust.json()["id"],
        "inner_user_id": user_r.json()["id"],
    }


@pytest.fixture(scope="module")
def org_b_headers(client: TestClient) -> dict[str, str]:
    """Org B — the attacker that should be denied access to Org A's data."""
    r = client.post(_api("/organizations/signup"), json=_signup_payload())
    assert r.status_code == 201, r.text
    return _auth(r.json()["access_token"])


# ---------------------------------------------------------------------------
# Category isolation
# ---------------------------------------------------------------------------


def test_category_list_does_not_leak_other_org(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    """Org B's category list must not contain Org A's categories."""
    r = client.get(_api("/categories/"), headers=org_b_headers)
    assert r.status_code == 200
    ids = [c["id"] for c in r.json()["data"]]
    assert org_a["category_id"] not in ids


def test_category_get_by_id_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.get(_api(f"/categories/{org_a['category_id']}"), headers=org_b_headers)
    assert r.status_code == 404


def test_category_update_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.patch(
        _api(f"/categories/{org_a['category_id']}"),
        headers=org_b_headers,
        json={"name": "Hacked"},
    )
    assert r.status_code == 404


def test_category_delete_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.delete(
        _api(f"/categories/{org_a['category_id']}"), headers=org_b_headers
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Product isolation
# ---------------------------------------------------------------------------


def test_product_list_does_not_leak_other_org(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.get(_api("/products/"), headers=org_b_headers)
    assert r.status_code == 200
    ids = [p["id"] for p in r.json()["data"]]
    assert org_a["product_id"] not in ids


def test_product_get_by_id_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.get(_api(f"/products/{org_a['product_id']}"), headers=org_b_headers)
    assert r.status_code == 404


def test_product_update_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.patch(
        _api(f"/products/{org_a['product_id']}"),
        headers=org_b_headers,
        json={"name": "Stolen"},
    )
    assert r.status_code == 404


def test_product_delete_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.delete(
        _api(f"/products/{org_a['product_id']}"), headers=org_b_headers
    )
    assert r.status_code == 404


def test_product_stock_adjust_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.post(
        _api(f"/products/{org_a['product_id']}/adjust-stock"),
        headers=org_b_headers,
        json={"quantity": 100, "reason": "theft attempt"},
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Customer isolation
# ---------------------------------------------------------------------------


def test_customer_list_does_not_leak_other_org(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.get(_api("/customers/"), headers=org_b_headers)
    assert r.status_code == 200
    ids = [c["id"] for c in r.json()["data"]]
    assert org_a["customer_id"] not in ids


def test_customer_get_by_id_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.get(_api(f"/customers/{org_a['customer_id']}"), headers=org_b_headers)
    assert r.status_code == 404


def test_customer_update_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.patch(
        _api(f"/customers/{org_a['customer_id']}"),
        headers=org_b_headers,
        json={"first_name": "Hacked"},
    )
    assert r.status_code == 404


def test_customer_delete_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.delete(
        _api(f"/customers/{org_a['customer_id']}"), headers=org_b_headers
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# User isolation
# ---------------------------------------------------------------------------


def test_user_list_does_not_leak_other_org(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.get(_api("/users/"), headers=org_b_headers)
    assert r.status_code == 200
    ids = [u["id"] for u in r.json()["data"]]
    assert org_a["inner_user_id"] not in ids


def test_user_get_by_id_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.get(_api(f"/users/{org_a['inner_user_id']}"), headers=org_b_headers)
    assert r.status_code == 404


def test_user_update_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.patch(
        _api(f"/users/{org_a['inner_user_id']}"),
        headers=org_b_headers,
        json={"first_name": "Hacked"},
    )
    assert r.status_code == 404


def test_user_delete_cross_org_returns_404(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    r = client.delete(
        _api(f"/users/{org_a['inner_user_id']}"), headers=org_b_headers
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Organization isolation
# ---------------------------------------------------------------------------


def test_get_my_organization_returns_own_org(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    """Each org's /organizations/me returns its own org, not the other's."""
    org_a_r = client.get(_api("/organizations/me"), headers=org_a["headers"])
    org_b_r = client.get(_api("/organizations/me"), headers=org_b_headers)
    assert org_a_r.status_code == 200
    assert org_b_r.status_code == 200
    assert org_a_r.json()["id"] != org_b_r.json()["id"]


def test_org_b_cannot_update_org_a_via_me(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    """PATCH /organizations/me always targets own org — Org B can't reach Org A."""
    # Org A's current name before Org B attempts anything
    before = client.get(_api("/organizations/me"), headers=org_a["headers"]).json()["name"]

    # Org B patches its own org (not Org A's)
    client.patch(
        _api("/organizations/me"),
        headers=org_b_headers,
        json={"name": "I am Org A now"},
    )

    # Org A's name must be unchanged
    after = client.get(_api("/organizations/me"), headers=org_a["headers"]).json()["name"]
    assert before == after


# ---------------------------------------------------------------------------
# Dashboard isolation
# ---------------------------------------------------------------------------


def test_dashboard_stats_scoped_to_own_org(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    """Dashboard stats endpoint must only reflect the requesting org's data."""
    r_a = client.get(_api("/dashboard/stats"), headers=org_a["headers"])
    r_b = client.get(_api("/dashboard/stats"), headers=org_b_headers)
    assert r_a.status_code == 200
    assert r_b.status_code == 200
    # Org B has no sales — its monthly total and average ticket must be 0
    body_b = r_b.json()
    assert float(body_b["sales_month"]["total"]) == 0.0
    assert float(body_b["average_ticket"]) == 0.0
    assert body_b["top_products_by_revenue"] == []


def test_dashboard_low_stock_scoped_to_own_org(
    client: TestClient, org_a: dict, org_b_headers: dict[str, str]
) -> None:
    # Low-stock lives under /products/low-stock, scoped to current org
    r = client.get(_api("/products/low-stock"), headers=org_b_headers)
    assert r.status_code == 200
    # Org A's product must not appear in Org B's low-stock list
    ids = [p["id"] for p in r.json()["data"]]
    assert org_a["product_id"] not in ids


# ---------------------------------------------------------------------------
# Token cannot be forged to switch org
# ---------------------------------------------------------------------------


def test_expired_or_tampered_token_is_rejected(client: TestClient) -> None:
    """A garbage token must not grant access to any org's data."""
    headers = {"Authorization": "Bearer this.is.not.a.valid.jwt"}
    r = client.get(_api("/products/"), headers=headers)
    assert r.status_code == 403


def test_missing_token_is_rejected(client: TestClient) -> None:
    r = client.get(_api("/products/"))
    assert r.status_code == 401

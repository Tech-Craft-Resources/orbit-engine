from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app import crud
from app.core.config import settings
from app.models import User


def test_create_user(client: TestClient, db: Session) -> None:
    # Get the default organization for testing
    org = crud.get_organization_by_slug(session=db, slug="default")
    assert org, "Default organization must exist for tests"

    r = client.post(
        f"{settings.API_V1_STR}/private/users/",
        json={
            "email": "pollo@listo.com",
            "password": "password123",
            "first_name": "Pollo",
            "last_name": "Listo",
            "organization_id": str(org.id),
            "role_id": 3,  # viewer
        },
    )

    assert r.status_code == 200

    data = r.json()

    user = db.exec(select(User).where(User.id == data["id"])).first()

    assert user
    assert user.email == "pollo@listo.com"
    assert user.first_name == "Pollo"
    assert user.last_name == "Listo"

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import User, Category, Product, Customer, InventoryMovement, SaleItem, Sale
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        # Cleanup test data (keep the superuser and default org)
        # Order matters: sale_items reference sales, sales reference products/customers/users,
        # movements reference products/users, products reference categories
        statement = delete(SaleItem)
        session.execute(statement)
        statement = delete(Sale)
        session.execute(statement)
        statement = delete(InventoryMovement)
        session.execute(statement)
        statement = delete(Product)
        session.execute(statement)
        statement = delete(Customer)
        session.execute(statement)
        statement = delete(Category)
        session.execute(statement)
        statement = delete(User).where(User.email != settings.FIRST_SUPERUSER)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )

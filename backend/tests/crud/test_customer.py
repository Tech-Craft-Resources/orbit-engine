import uuid

from sqlmodel import Session

from app import crud
from app.models import CustomerCreate, CustomerUpdate
from tests.utils.customer import create_random_customer
from tests.utils.user import _get_default_org_id
from tests.utils.utils import random_lower_string


def test_create_customer(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    doc_number = f"DOC-{random_lower_string()[:16]}"
    customer_in = CustomerCreate(
        document_type="DNI",
        document_number=doc_number,
        first_name="Juan",
        last_name="Pérez",
        email="juan@test.com",
        phone="555-0100",
    )
    customer = crud.create_customer(
        session=db, customer_create=customer_in, organization_id=organization_id
    )
    assert customer.document_type == "DNI"
    assert customer.document_number == doc_number
    assert customer.first_name == "Juan"
    assert customer.last_name == "Pérez"
    assert customer.organization_id == organization_id
    assert customer.is_active is True
    assert customer.deleted_at is None
    assert customer.total_purchases == 0
    assert customer.purchases_count == 0


def test_get_customer_by_id(db: Session) -> None:
    customer = create_random_customer(db)
    fetched = crud.get_customer_by_id(
        session=db,
        customer_id=customer.id,
        organization_id=customer.organization_id,
    )
    assert fetched
    assert fetched.id == customer.id
    assert fetched.document_number == customer.document_number


def test_get_customer_by_id_not_found(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    fetched = crud.get_customer_by_id(
        session=db,
        customer_id=uuid.uuid4(),
        organization_id=organization_id,
    )
    assert fetched is None


def test_get_customers_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    create_random_customer(db, organization_id=organization_id)
    create_random_customer(db, organization_id=organization_id)
    customers = crud.get_customers_by_organization(
        session=db, organization_id=organization_id
    )
    assert len(customers) >= 2


def test_count_customers_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    count = crud.count_customers_by_organization(
        session=db, organization_id=organization_id
    )
    assert count >= 0


def test_get_customer_by_document(db: Session) -> None:
    customer = create_random_customer(db)
    fetched = crud.get_customer_by_document(
        session=db,
        document_number=customer.document_number,
        organization_id=customer.organization_id,
    )
    assert fetched
    assert fetched.id == customer.id


def test_update_customer(db: Session) -> None:
    customer = create_random_customer(db)
    update_data = CustomerUpdate(
        first_name="Updated",
        last_name="Name",
        email="updated@test.com",
    )
    updated = crud.update_customer(
        session=db, db_customer=customer, customer_in=update_data
    )
    assert updated.first_name == "Updated"
    assert updated.last_name == "Name"
    assert updated.email == "updated@test.com"


def test_soft_delete_customer(db: Session) -> None:
    customer = create_random_customer(db)
    deleted = crud.soft_delete_customer(session=db, db_customer=customer)
    assert deleted.deleted_at is not None
    assert deleted.is_active is False

    # Should not appear in normal queries
    fetched = crud.get_customer_by_id(
        session=db,
        customer_id=customer.id,
        organization_id=customer.organization_id,
    )
    assert fetched is None

import uuid

from sqlmodel import Session

from app import crud
from app.models import Customer, CustomerCreate
from tests.utils.user import _get_default_org_id
from tests.utils.utils import random_lower_string


def create_random_customer(
    db: Session,
    *,
    organization_id: uuid.UUID | None = None,
) -> Customer:
    """Create a random customer for testing."""
    if organization_id is None:
        organization_id = _get_default_org_id(db)
    doc_number = f"DOC-{random_lower_string()[:16]}"
    customer_in = CustomerCreate(
        document_type="DNI",
        document_number=doc_number,
        first_name="Test",
        last_name="Customer",
        email=f"{random_lower_string()[:10]}@test.com",
        phone="555-0100",
    )
    return crud.create_customer(
        session=db, customer_create=customer_in, organization_id=organization_id
    )

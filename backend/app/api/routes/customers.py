import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.deps import (
    CurrentOrganization,
    CurrentUser,
    SessionDep,
    require_role,
)
from app.models import (
    CustomerCreate,
    CustomerPublic,
    CustomersPublic,
    CustomerUpdate,
    Message,
    SalesPublic,
)

router = APIRouter()


@router.get("/", response_model=CustomersPublic)
def read_customers(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve customers in current organization.

    Admin and seller roles can list customers.
    """
    customers = crud.get_customers_by_organization(
        session=session, organization_id=current_organization, skip=skip, limit=limit
    )
    count = crud.count_customers_by_organization(
        session=session, organization_id=current_organization
    )
    return CustomersPublic(data=customers, count=count)


@router.post(
    "/",
    response_model=CustomerPublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def create_customer(
    *,
    session: SessionDep,
    current_organization: CurrentOrganization,
    customer_in: CustomerCreate,
) -> Any:
    """
    Create a new customer in current organization.

    Only admin and seller roles can create customers.
    """
    # Check for duplicate document number within organization
    existing = crud.get_customer_by_document(
        session=session,
        document_number=customer_in.document_number,
        organization_id=current_organization,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A customer with this document number already exists in the organization",
        )

    customer = crud.create_customer(
        session=session,
        customer_create=customer_in,
        organization_id=current_organization,
    )
    return customer


@router.get("/{customer_id}", response_model=CustomerPublic)
def read_customer(
    customer_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Get a specific customer by ID.

    Admin and seller roles can view a customer.
    """
    customer = crud.get_customer_by_id(
        session=session,
        customer_id=customer_id,
        organization_id=current_organization,
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.patch(
    "/{customer_id}",
    response_model=CustomerPublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def update_customer(
    *,
    session: SessionDep,
    current_organization: CurrentOrganization,
    customer_id: uuid.UUID,
    customer_in: CustomerUpdate,
) -> Any:
    """
    Update a customer.

    Only admin and seller roles can update customers.
    """
    db_customer = crud.get_customer_by_id(
        session=session,
        customer_id=customer_id,
        organization_id=current_organization,
    )
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Check for duplicate document number if it's being changed
    if (
        customer_in.document_number is not None
        and customer_in.document_number != db_customer.document_number
    ):
        existing = crud.get_customer_by_document(
            session=session,
            document_number=customer_in.document_number,
            organization_id=current_organization,
        )
        if existing:
            raise HTTPException(
                status_code=409,
                detail="A customer with this document number already exists in the organization",
            )

    customer = crud.update_customer(
        session=session, db_customer=db_customer, customer_in=customer_in
    )
    return customer


@router.delete(
    "/{customer_id}",
    response_model=Message,
    dependencies=[Depends(require_role("admin"))],
)
def delete_customer(
    customer_id: uuid.UUID,
    session: SessionDep,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Delete a customer (soft delete).

    Only admin users can delete customers.
    """
    db_customer = crud.get_customer_by_id(
        session=session,
        customer_id=customer_id,
        organization_id=current_organization,
    )
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    crud.soft_delete_customer(session=session, db_customer=db_customer)
    return Message(message="Customer deleted successfully")


@router.get("/{customer_id}/sales", response_model=SalesPublic)
def read_customer_sales(
    customer_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get sales for a specific customer.

    Any authenticated user can view a customer's sales.
    """
    customer = crud.get_customer_by_id(
        session=session,
        customer_id=customer_id,
        organization_id=current_organization,
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    sales = crud.get_sales_by_customer(
        session=session,
        customer_id=customer_id,
        organization_id=current_organization,
        skip=skip,
        limit=limit,
    )
    count = crud.count_sales_by_customer(
        session=session,
        customer_id=customer_id,
        organization_id=current_organization,
    )
    return SalesPublic(data=sales, count=count)

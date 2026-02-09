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
    CategoriesPublic,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
    Message,
)

router = APIRouter()


@router.get("/", response_model=CategoriesPublic)
def read_categories(
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve categories in current organization.

    Any authenticated user can list categories.
    """
    categories = crud.get_categories_by_organization(
        session=session, organization_id=current_organization, skip=skip, limit=limit
    )
    count = crud.count_categories_by_organization(
        session=session, organization_id=current_organization
    )
    return CategoriesPublic(data=categories, count=count)


@router.post(
    "/",
    response_model=CategoryPublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def create_category(
    *,
    session: SessionDep,
    current_organization: CurrentOrganization,
    category_in: CategoryCreate,
) -> Any:
    """
    Create a new category in current organization.

    Only admin and seller roles can create categories.
    """
    # Validate parent_id if provided
    if category_in.parent_id is not None:
        parent = crud.get_category_by_id(
            session=session,
            category_id=category_in.parent_id,
            organization_id=current_organization,
        )
        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent category not found",
            )

    # Check for duplicate name within same parent
    existing = crud.get_category_by_name(
        session=session,
        name=category_in.name,
        organization_id=current_organization,
        parent_id=category_in.parent_id,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A category with this name already exists in the same level",
        )

    category = crud.create_category(
        session=session,
        category_create=category_in,
        organization_id=current_organization,
    )
    return category


@router.get("/{category_id}", response_model=CategoryPublic)
def read_category(
    category_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Get a specific category by ID.

    Any authenticated user can view a category.
    """
    category = crud.get_category_by_id(
        session=session,
        category_id=category_id,
        organization_id=current_organization,
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch(
    "/{category_id}",
    response_model=CategoryPublic,
    dependencies=[Depends(require_role("admin", "seller"))],
)
def update_category(
    *,
    session: SessionDep,
    current_organization: CurrentOrganization,
    category_id: uuid.UUID,
    category_in: CategoryUpdate,
) -> Any:
    """
    Update a category.

    Only admin and seller roles can update categories.
    """
    db_category = crud.get_category_by_id(
        session=session,
        category_id=category_id,
        organization_id=current_organization,
    )
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Validate parent_id if provided
    if category_in.parent_id is not None:
        if category_in.parent_id == category_id:
            raise HTTPException(
                status_code=400,
                detail="A category cannot be its own parent",
            )
        parent = crud.get_category_by_id(
            session=session,
            category_id=category_in.parent_id,
            organization_id=current_organization,
        )
        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent category not found",
            )

    # Check for duplicate name if name is being changed
    if category_in.name is not None:
        # Determine the effective parent_id for uniqueness check
        effective_parent_id = (
            category_in.parent_id
            if category_in.parent_id is not None
            else db_category.parent_id
        )
        existing = crud.get_category_by_name(
            session=session,
            name=category_in.name,
            organization_id=current_organization,
            parent_id=effective_parent_id,
        )
        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=409,
                detail="A category with this name already exists in the same level",
            )

    category = crud.update_category(
        session=session, db_category=db_category, category_in=category_in
    )
    return category


@router.delete(
    "/{category_id}",
    response_model=Message,
    dependencies=[Depends(require_role("admin"))],
)
def delete_category(
    category_id: uuid.UUID,
    session: SessionDep,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Delete a category (soft delete).

    Only admin users can delete categories.
    """
    db_category = crud.get_category_by_id(
        session=session,
        category_id=category_id,
        organization_id=current_organization,
    )
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    crud.soft_delete_category(session=session, db_category=db_category)
    return Message(message="Category deleted successfully")

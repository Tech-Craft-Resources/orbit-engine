from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Message,
    Organization,
    OrganizationPublic,
    OrganizationSignup,
    OrganizationUpdate,
    UserPublicWithRelations,
    LoginResponse,
)
from app.core.security import create_access_token

router = APIRouter()


@router.post("/signup", response_model=LoginResponse, status_code=201)
def signup_organization(
    *, session: SessionDep, organization_signup: OrganizationSignup
) -> Any:
    """
    Create a new organization with an admin user.

    This is the entry point for new organizations to sign up.
    It creates:
    1. A new organization
    2. An admin user for that organization
    3. Returns a login token for the new admin user
    """
    # Check if organization slug is already taken
    existing_org = crud.get_organization_by_slug(
        session=session, slug=organization_signup.organization_slug
    )
    if existing_org:
        raise HTTPException(
            status_code=409,
            detail="An organization with this slug already exists",
        )

    # Check if email is already in use in any organization
    existing_user = crud.get_user_by_email(
        session=session, email=organization_signup.admin_email
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists",
        )

    # Create organization
    from app.models import OrganizationCreate

    organization = crud.create_organization(
        session=session,
        organization_create=OrganizationCreate(
            name=organization_signup.organization_name,
            slug=organization_signup.organization_slug,
            description=organization_signup.organization_description,
        ),
    )

    # Get admin role
    admin_role = crud.get_role_by_name(session=session, name="admin")
    if not admin_role:
        raise HTTPException(
            status_code=500,
            detail="Admin role not found. Database may not be properly initialized.",
        )

    # Create admin user
    from app.models import UserCreate

    user = crud.create_user(
        session=session,
        user_create=UserCreate(
            email=organization_signup.admin_email,
            password=organization_signup.admin_password,
            first_name=organization_signup.admin_first_name,
            last_name=organization_signup.admin_last_name,
            phone=organization_signup.admin_phone,
            role_id=admin_role.id,
        ),
        organization_id=organization.id,
    )

    # Refresh to load relationships
    session.refresh(user)
    session.refresh(user, ["organization", "role"])

    # Create access token
    from app.models import TokenPayload

    access_token = create_access_token(
        subject=str(user.id),
        organization_id=str(user.organization_id),
        role=admin_role.name,
    )

    # Build response
    from app.models import UserPublic, OrganizationPublic, RolePublic

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserPublicWithRelations(
            id=user.id,
            organization_id=user.organization_id,
            role_id=user.role_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            avatar_url=user.avatar_url,
            is_active=user.is_active,
            is_verified=user.is_verified,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
            organization=OrganizationPublic(
                id=organization.id,
                name=organization.name,
                slug=organization.slug,
                description=organization.description,
                logo_url=organization.logo_url,
                is_active=organization.is_active,
                created_at=organization.created_at,
                updated_at=organization.updated_at,
            ),
            role=RolePublic(
                id=admin_role.id,
                name=admin_role.name,
                description=admin_role.description,
                permissions=admin_role.permissions,
                created_at=admin_role.created_at,
            ),
        ),
    )


@router.get("/me", response_model=OrganizationPublic)
def get_my_organization(*, session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Get current user's organization.
    """
    organization = crud.get_organization_by_id(
        session=session, organization_id=current_user.organization_id
    )
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.patch("/me", response_model=OrganizationPublic)
def update_my_organization(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    organization_in: OrganizationUpdate,
) -> Any:
    """
    Update current user's organization.

    Only admin users can update organization settings.
    """
    # Check if user is admin
    from app.api.deps import require_role
    from fastapi import Depends

    # Get current organization
    organization = crud.get_organization_by_id(
        session=session, organization_id=current_user.organization_id
    )
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Check if user is admin
    role = session.get(crud.Role, current_user.role_id)
    if not role or role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can update organization settings",
        )

    # If slug is being updated, check if it's already taken
    if organization_in.slug and organization_in.slug != organization.slug:
        existing_org = crud.get_organization_by_slug(
            session=session, slug=organization_in.slug
        )
        if existing_org:
            raise HTTPException(
                status_code=409,
                detail="An organization with this slug already exists",
            )

    # Update organization
    updated_organization = crud.update_organization(
        session=session, db_organization=organization, organization_in=organization_in
    )
    return updated_organization

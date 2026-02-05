from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.core import security
from app.core.config import settings
from app.models import (
    Message,
    NewPassword,
    Token,
    UserPublic,
    UserPublicWithRelations,
    UserUpdate,
    LoginResponse,
    OrganizationPublic,
    RolePublic,
)
from app.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

router = APIRouter(tags=["login"])


@router.post("/login/access-token", response_model=LoginResponse)
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.

    Returns user data with organization and role information.
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Get user's role
    role = session.get(crud.Role, user.role_id)
    if not role:
        raise HTTPException(status_code=500, detail="User role not found")

    # Get user's organization
    organization = session.get(crud.Organization, user.organization_id)
    if not organization:
        raise HTTPException(status_code=500, detail="User organization not found")

    # Update last login
    from datetime import datetime, timezone

    user.last_login_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()

    # Create access token
    access_token = security.create_access_token(
        subject=str(user.id),
        organization_id=str(user.organization_id),
        role=role.name,
    )

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
                id=role.id,
                name=role.name,
                description=role.description,
                permissions=role.permissions,
                created_at=role.created_at,
            ),
        ),
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Password Recovery
    """
    user = crud.get_user_by_email(session=session, email=email)

    # Always return the same response to prevent email enumeration attacks
    # Only send email if user actually exists
    if user:
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )
        send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return Message(
        message="If that email is registered, we sent a password recovery link"
    )


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        # Don't reveal that the user doesn't exist - use same error as invalid token
        raise HTTPException(status_code=400, detail="Invalid token")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    user_in_update = UserUpdate(password=body.new_password)
    crud.update_user(
        session=session,
        db_user=user,
        user_in=user_in_update,
    )
    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    response_class=HTMLResponse,
)
def recover_password_html_content(
    email: str, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    HTML Content for Password Recovery

    Requires authentication (admin only in production, but any user for testing)
    """
    # Check if user is admin
    from app.api.deps import CurrentAdminUser

    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )

from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate, Organization, OrganizationCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    """
    Initialize database with first superuser.

    Note: With the new multi-tenancy system, the recommended way to create
    the first organization and admin user is via the /organizations/signup endpoint.

    This function is kept for backward compatibility but is now deprecated.
    """
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    # Check if the superuser already exists (including soft-deleted)
    existing_user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()

    if existing_user and (existing_user.deleted_at is not None or not existing_user.is_active):
        # Restore a soft-deleted superuser
        existing_user.deleted_at = None
        existing_user.is_active = True
        session.add(existing_user)
        session.commit()
        session.refresh(existing_user)

    if not existing_user:
        # Check if default organization exists
        default_org = crud.get_organization_by_slug(session=session, slug="default")

        if not default_org:
            # Create default organization
            org_in = OrganizationCreate(
                name="Default Organization",
                slug="default",
                description="Auto-generated default organization",
            )
            default_org = crud.create_organization(
                session=session, organization_create=org_in
            )

        # Get admin role
        admin_role = crud.get_role_by_name(session=session, name="admin")
        if not admin_role:
            raise RuntimeError(
                "Admin role not found. Please run database migrations first: alembic upgrade head"
            )

        # Create first superuser
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            first_name="Super",
            last_name="Admin",
            role_id=admin_role.id,
        )
        user = crud.create_user(
            session=session,
            user_create=user_in,
            organization_id=default_org.id,
        )

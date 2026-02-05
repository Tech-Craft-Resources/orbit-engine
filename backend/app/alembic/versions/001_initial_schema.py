"""Initial schema with organizations, roles and users

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-02-05 18:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create organizations table
    op.create_table(
        "organizations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("logo_url", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.create_index("idx_organizations_slug", "organizations", ["slug"], unique=True)
    op.create_index("idx_organizations_is_active", "organizations", ["is_active"])

    # Create roles table
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("permissions", JSONB, nullable=False, server_default="[]"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.create_index("idx_roles_name", "roles", ["name"], unique=True)

    # Insert default roles
    op.execute(
        """
        INSERT INTO roles (id, name, description, permissions) VALUES
        (1, 'admin', 'Administrator with full access', '["*"]'::jsonb),
        (2, 'seller', 'Seller with access to sales and inventory', '["sales.*", "inventory.read", "customers.*"]'::jsonb),
        (3, 'viewer', 'Read-only access to reports and dashboard', '["reports.read", "dashboard.read"]'::jsonb)
        """
    )

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "role_id",
            sa.Integer(),
            sa.ForeignKey("roles.id"),
            nullable=False,
        ),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "failed_login_attempts", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Create indexes and constraints for users
    op.create_index("idx_users_organization_id", "users", ["organization_id"])
    op.create_index("idx_users_role_id", "users", ["role_id"])
    op.create_index("idx_users_is_active", "users", ["is_active"])
    op.create_index(
        "idx_users_email", "users", ["email"]
    )  # Non-unique index for general searches

    # Unique constraint on organization_id + email (enforces unique email per org)
    op.create_index(
        "uq_users_organization_email",
        "users",
        ["organization_id", "email"],
        unique=True,
    )


def downgrade():
    # Drop in reverse order
    op.drop_index("uq_users_organization_email", table_name="users")
    op.drop_index("idx_users_email", table_name="users")
    op.drop_index("idx_users_is_active", table_name="users")
    op.drop_index("idx_users_role_id", table_name="users")
    op.drop_index("idx_users_organization_id", table_name="users")
    op.drop_table("users")

    op.drop_index("idx_roles_name", table_name="roles")
    op.drop_table("roles")

    op.drop_index("idx_organizations_is_active", table_name="organizations")
    op.drop_index("idx_organizations_slug", table_name="organizations")
    op.drop_table("organizations")

"""Add categories table

Revision ID: 002_categories
Revises: 001_initial_schema
Create Date: 2026-02-08 22:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "002_categories"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "parent_id",
            UUID(as_uuid=True),
            sa.ForeignKey("categories.id", ondelete="SET NULL"),
            nullable=True,
        ),
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
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Indexes
    op.create_index("idx_categories_organization_id", "categories", ["organization_id"])
    op.create_index("idx_categories_parent_id", "categories", ["parent_id"])
    op.create_index("idx_categories_is_active", "categories", ["is_active"])

    # Unique constraint: name must be unique per organization + parent
    # (allows same name in different parents or different orgs)
    op.create_index(
        "uq_categories_organization_name_parent",
        "categories",
        ["organization_id", "name", "parent_id"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        "uq_categories_organization_name_parent", table_name="categories"
    )
    op.drop_index("idx_categories_is_active", table_name="categories")
    op.drop_index("idx_categories_parent_id", table_name="categories")
    op.drop_index("idx_categories_organization_id", table_name="categories")
    op.drop_table("categories")

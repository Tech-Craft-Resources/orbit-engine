"""Add customers table

Revision ID: 004_customers
Revises: 003_products
Create Date: 2026-02-08 23:30:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "004_customers"
down_revision = "003_products"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "customers",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("document_type", sa.String(length=50), nullable=False),
        sa.Column("document_number", sa.String(length=50), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "total_purchases",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "purchases_count", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "last_purchase_at", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default="true"
        ),
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
    op.create_index(
        "idx_customers_organization_id", "customers", ["organization_id"]
    )
    op.create_index("idx_customers_email", "customers", ["email"])
    op.create_index("idx_customers_phone", "customers", ["phone"])
    op.create_index("idx_customers_is_active", "customers", ["is_active"])

    # Unique constraint: document_number must be unique per organization
    op.create_index(
        "uq_customers_organization_document",
        "customers",
        ["organization_id", "document_number"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        "uq_customers_organization_document", table_name="customers"
    )
    op.drop_index("idx_customers_is_active", table_name="customers")
    op.drop_index("idx_customers_phone", table_name="customers")
    op.drop_index("idx_customers_email", table_name="customers")
    op.drop_index("idx_customers_organization_id", table_name="customers")
    op.drop_table("customers")

"""Add products table

Revision ID: 003_products
Revises: 002_categories
Create Date: 2026-02-08 23:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "003_products"
down_revision = "002_categories"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "category_id",
            UUID(as_uuid=True),
            sa.ForeignKey("categories.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column(
            "cost_price",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "sale_price",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "stock_quantity", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("stock_min", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("stock_max", sa.Integer(), nullable=True),
        sa.Column(
            "unit", sa.String(length=50), nullable=False, server_default="unit"
        ),
        sa.Column("barcode", sa.String(length=100), nullable=True),
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
        "idx_products_organization_id", "products", ["organization_id"]
    )
    op.create_index("idx_products_category_id", "products", ["category_id"])
    op.create_index("idx_products_is_active", "products", ["is_active"])
    op.create_index("idx_products_sku", "products", ["sku"])

    # Unique constraint: SKU must be unique per organization
    op.create_index(
        "uq_products_organization_sku",
        "products",
        ["organization_id", "sku"],
        unique=True,
    )


def downgrade():
    op.drop_index("uq_products_organization_sku", table_name="products")
    op.drop_index("idx_products_sku", table_name="products")
    op.drop_index("idx_products_is_active", table_name="products")
    op.drop_index("idx_products_category_id", table_name="products")
    op.drop_index("idx_products_organization_id", table_name="products")
    op.drop_table("products")

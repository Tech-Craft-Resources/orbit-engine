"""Add sales and sale_items tables

Revision ID: 006_sales
Revises: 005_inventory_movements
Create Date: 2026-02-08 23:50:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "006_sales"
down_revision = "005_inventory_movements"
branch_labels = None
depends_on = None


def upgrade():
    # --- Sales table ---
    op.create_table(
        "sales",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "customer_id",
            UUID(as_uuid=True),
            sa.ForeignKey("customers.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("invoice_number", sa.String(length=100), nullable=False),
        sa.Column(
            "sale_date",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "subtotal",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "discount",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "tax",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "total",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="0",
        ),
        sa.Column("payment_method", sa.String(length=50), nullable=False, server_default="cash"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="completed"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "cancelled_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "cancelled_by",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("cancellation_reason", sa.Text(), nullable=True),
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

    # Unique constraint: invoice_number per organization
    op.create_unique_constraint(
        "uq_sales_organization_invoice_number",
        "sales",
        ["organization_id", "invoice_number"],
    )

    # Indexes for sales
    op.create_index("idx_sales_organization_id", "sales", ["organization_id"])
    op.create_index("idx_sales_customer_id", "sales", ["customer_id"])
    op.create_index("idx_sales_user_id", "sales", ["user_id"])
    op.create_index("idx_sales_status", "sales", ["status"])
    op.create_index("idx_sales_sale_date", "sales", ["sale_date"])
    op.create_index("idx_sales_invoice_number", "sales", ["invoice_number"])

    # --- Sale Items table ---
    op.create_table(
        "sale_items",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "sale_id",
            UUID(as_uuid=True),
            sa.ForeignKey("sales.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "product_id",
            UUID(as_uuid=True),
            sa.ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("product_name", sa.String(length=255), nullable=False),
        sa.Column("product_sku", sa.String(length=100), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column(
            "unit_price",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "subtotal",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        # Check constraints
        sa.CheckConstraint("quantity > 0", name="ck_sale_items_quantity_positive"),
        sa.CheckConstraint("unit_price >= 0", name="ck_sale_items_unit_price_non_negative"),
        sa.CheckConstraint("subtotal >= 0", name="ck_sale_items_subtotal_non_negative"),
    )

    # Indexes for sale_items
    op.create_index("idx_sale_items_sale_id", "sale_items", ["sale_id"])
    op.create_index("idx_sale_items_product_id", "sale_items", ["product_id"])


def downgrade():
    # Drop sale_items first (FK dependency)
    op.drop_index("idx_sale_items_product_id", table_name="sale_items")
    op.drop_index("idx_sale_items_sale_id", table_name="sale_items")
    op.drop_table("sale_items")

    # Drop sales
    op.drop_index("idx_sales_invoice_number", table_name="sales")
    op.drop_index("idx_sales_sale_date", table_name="sales")
    op.drop_index("idx_sales_status", table_name="sales")
    op.drop_index("idx_sales_user_id", table_name="sales")
    op.drop_index("idx_sales_customer_id", table_name="sales")
    op.drop_index("idx_sales_organization_id", table_name="sales")
    op.drop_constraint("uq_sales_organization_invoice_number", "sales", type_="unique")
    op.drop_table("sales")

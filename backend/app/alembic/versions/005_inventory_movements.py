"""Add inventory_movements table

Revision ID: 005_inventory_movements
Revises: 004_customers
Create Date: 2026-02-08 23:45:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "005_inventory_movements"
down_revision = "004_customers"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "inventory_movements",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "product_id",
            UUID(as_uuid=True),
            sa.ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("movement_type", sa.String(length=50), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("previous_stock", sa.Integer(), nullable=False),
        sa.Column("new_stock", sa.Integer(), nullable=False),
        sa.Column("reference_id", UUID(as_uuid=True), nullable=True),
        sa.Column("reference_type", sa.String(length=50), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    # Indexes
    op.create_index(
        "idx_inventory_movements_organization_id",
        "inventory_movements",
        ["organization_id"],
    )
    op.create_index(
        "idx_inventory_movements_product_id",
        "inventory_movements",
        ["product_id"],
    )
    op.create_index(
        "idx_inventory_movements_user_id",
        "inventory_movements",
        ["user_id"],
    )
    op.create_index(
        "idx_inventory_movements_movement_type",
        "inventory_movements",
        ["movement_type"],
    )
    op.create_index(
        "idx_inventory_movements_created_at",
        "inventory_movements",
        ["created_at"],
    )
    op.create_index(
        "idx_inventory_movements_reference",
        "inventory_movements",
        ["reference_type", "reference_id"],
    )


def downgrade():
    op.drop_index(
        "idx_inventory_movements_reference", table_name="inventory_movements"
    )
    op.drop_index(
        "idx_inventory_movements_created_at", table_name="inventory_movements"
    )
    op.drop_index(
        "idx_inventory_movements_movement_type", table_name="inventory_movements"
    )
    op.drop_index(
        "idx_inventory_movements_user_id", table_name="inventory_movements"
    )
    op.drop_index(
        "idx_inventory_movements_product_id", table_name="inventory_movements"
    )
    op.drop_index(
        "idx_inventory_movements_organization_id",
        table_name="inventory_movements",
    )
    op.drop_table("inventory_movements")

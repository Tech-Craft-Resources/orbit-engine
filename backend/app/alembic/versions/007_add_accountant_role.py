"""Add contador role for exports

Revision ID: 007_add_accountant_role
Revises: 006_sales
Create Date: 2026-04-07 12:00:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "007_add_accountant_role"
down_revision = "006_sales"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO roles (id, name, description, permissions)
        VALUES (4, 'contador', 'Accountant with export access', '["dashboard.read", "dashboard.export"]'::jsonb)
        ON CONFLICT (id) DO NOTHING;
        """
    )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE id = 4 AND name = 'contador';")

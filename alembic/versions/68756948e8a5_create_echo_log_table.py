"""create echo_log table

Revision ID: 68756948e8a5
Revises: 
Create Date: 2023-08-28 21:06:53.129212

"""
from alembic import op
import sqlalchemy as sa


revision = "68756948e8a5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "echo_log",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("message", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False),
    )


def downgrade():
    op.drop_table("echo_log")

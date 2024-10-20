"""add users

Revision ID: 20c22c9c3217
Revises: 0f2f683866e6
Create Date: 2024-10-20 19:10:48.935144

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20c22c9c3217"
down_revision: Union[str, None] = "0f2f683866e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")

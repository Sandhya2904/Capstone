"""add optional location column

Revision ID: 20261127_002
Revises: 20261127_001
Create Date: 2026-11-27
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20261127_002"
down_revision: Union[str, None] = "20261127_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("devices", sa.Column("location", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("devices", "location")

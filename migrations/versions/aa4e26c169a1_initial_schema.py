"""Initial Schema.

Revision ID: aa4e26c169a1
Revises:
Create Date: 2020-01-24 15:27:05.487594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aa4e26c169a1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "credentials",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.String(length=32), nullable=False),
        sa.Column("email", sa.Text(), nullable=True),
        sa.Column("_password", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_credentials_uuid"), "credentials", ["uuid"], unique=True)
    op.create_table(
        "realms",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.String(length=32), nullable=False),
        sa.Column("slug", sa.Text(), nullable=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_realms_slug"), "realms", ["slug"], unique=True)
    op.create_index(op.f("ix_realms_uuid"), "realms", ["uuid"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_realms_uuid"), table_name="realms")
    op.drop_index(op.f("ix_realms_slug"), table_name="realms")
    op.drop_table("realms")
    op.drop_index(op.f("ix_credentials_uuid"), table_name="credentials")
    op.drop_table("credentials")

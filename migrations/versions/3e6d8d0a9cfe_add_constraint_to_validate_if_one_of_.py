"""Add constraint to validate if one of credential column is not null

Revision ID: 3e6d8d0a9cfe
Revises: 835549b518a2
Create Date: 2020-01-29 10:08:37.117163

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3e6d8d0a9cfe"
down_revision = "835549b518a2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "credentials",
        sa.Column("_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.alter_column("credentials", "citizen_id", existing_type=sa.TEXT(), nullable=True)
    op.alter_column("credentials", "email", existing_type=sa.TEXT(), nullable=True)
    op.alter_column("credentials", "msisdn", existing_type=sa.TEXT(), nullable=True)
    op.alter_column("credentials", "username", existing_type=sa.TEXT(), nullable=True)
    op.drop_column("credentials", "additional_data")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "credentials",
        sa.Column(
            "additional_data",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.alter_column("credentials", "username", existing_type=sa.TEXT(), nullable=False)
    op.alter_column("credentials", "msisdn", existing_type=sa.TEXT(), nullable=False)
    op.alter_column("credentials", "email", existing_type=sa.TEXT(), nullable=False)
    op.alter_column(
        "credentials", "citizen_id", existing_type=sa.TEXT(), nullable=False
    )
    op.drop_column("credentials", "_metadata")
    # ### end Alembic commands ###

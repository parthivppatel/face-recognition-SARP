"""create_table_face_data

Revision ID: e684ea44d25a
Revises: 
Create Date: 2023-07-15 11:19:55.465840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e684ea44d25a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('face_data',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('device_id', sa.String(length=255), nullable=False),
                    sa.Column('face_id', sa.String(length=255), nullable=True),
                    sa.Column('date', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('face_data')



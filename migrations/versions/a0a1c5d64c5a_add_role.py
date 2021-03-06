"""add role

Revision ID: a0a1c5d64c5a
Revises: b21d97b015b9
Create Date: 2022-03-04 19:44:15.887289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0a1c5d64c5a'
down_revision = 'b21d97b015b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_unique_constraint(None, 'author_model', ['surname'])
    op.add_column('user_model', sa.Column('role', sa.String(length=32), server_default='user', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_model', 'role')
    op.drop_constraint(None, 'author_model', type_='unique')
    # ### end Alembic commands ###

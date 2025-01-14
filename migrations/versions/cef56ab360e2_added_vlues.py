"""Added vlues

Revision ID: cef56ab360e2
Revises: 214304ad648f
Create Date: 2024-05-22 12:54:45.520919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cef56ab360e2'
down_revision = '214304ad648f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=False),
    sa.Column('icon_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('company_value')
    # ### end Alembic commands ###

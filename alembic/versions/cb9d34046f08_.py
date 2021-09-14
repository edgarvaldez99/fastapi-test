"""empty message

Revision ID: cb9d34046f08
Revises: e5cb8f2287a1
Create Date: 2021-09-13 22:24:51.216624

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cb9d34046f08'
down_revision = 'e5cb8f2287a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('audit_database', sa.Column('data_id', sa.BigInteger(), nullable=True))
    op.add_column('audit_database', sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.drop_column('audit_database', 'row')
    op.drop_column('audit_database', 'row_id')
    op.add_column('audit_request', sa.Column('user', sa.String(), nullable=True))
    op.add_column('audit_request', sa.Column('date_hour', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('audit_request', 'date_hour')
    op.drop_column('audit_request', 'user')
    op.add_column('audit_database', sa.Column('row_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.add_column('audit_database', sa.Column('row', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('audit_database', 'data')
    op.drop_column('audit_database', 'data_id')
    # ### end Alembic commands ###
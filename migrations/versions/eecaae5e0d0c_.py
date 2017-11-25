"""empty message

Revision ID: eecaae5e0d0c
Revises: 89aae6dbda42
Create Date: 2017-11-25 13:31:55.672634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eecaae5e0d0c'
down_revision = '89aae6dbda42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vehicle_types', 'id')
    op.drop_constraint('vehicles_type_fkey', 'vehicles', type_='foreignkey')
    op.create_foreign_key(None, 'vehicles', 'vehicle_types', ['type'], ['stara_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vehicles', type_='foreignkey')
    op.create_foreign_key('vehicles_type_fkey', 'vehicles', 'vehicle_types', ['type'], ['id'])
    op.add_column('vehicle_types', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('vehicle_types_id_seq'::regclass)"), nullable=False))
    # ### end Alembic commands ###

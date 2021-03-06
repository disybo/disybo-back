"""empty message

Revision ID: 221f71e43775
Revises: 57b1cd16ff7e
Create Date: 2017-11-26 00:43:46.802629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '221f71e43775'
down_revision = '57b1cd16ff7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicle_fuel_consumption',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fuel_card_num', sa.String(), nullable=True),
    sa.Column('vehicle_id', sa.String(length=6), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('consumption', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['fuel_card_num'], ['fuel_card_numbers.num'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.vehicle_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('vehicle_id', sa.VARCHAR(length=6), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('urgency', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.vehicle_id'], name='notifications_vehicle_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='notifications_pkey')
    )
    op.drop_table('vehicle_fuel_consumption')
    # ### end Alembic commands ###

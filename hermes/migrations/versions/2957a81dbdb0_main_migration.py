"""Main migration

Revision ID: 2957a81dbdb0
Revises: d3738344ff3e
Create Date: 2018-06-03 18:57:23.810624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2957a81dbdb0'
down_revision = 'd3738344ff3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_types',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('category', sa.Enum('client', 'provider', 'admin', name='usertypeenum'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('items',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('type_id', sa.String(), nullable=True),
    sa.Column('provier_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['provier_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['item_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('item_id', sa.String(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('addresses', sa.Column('area', sa.String(), nullable=True))
    op.add_column('addresses', sa.Column('city', sa.String(), nullable=True))
    op.add_column('addresses', sa.Column('country_id', sa.String(), nullable=True))
    op.add_column('addresses', sa.Column('notes', sa.String(), nullable=True))
    op.add_column('addresses', sa.Column('postal_code', sa.String(), nullable=True))
    op.add_column('addresses', sa.Column('street', sa.String(), nullable=False))
    op.add_column('addresses', sa.Column('street_num', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'addresses', 'countries', ['country_id'], ['id'])
    op.drop_column('addresses', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'addresses', type_='foreignkey')
    op.drop_column('addresses', 'street_num')
    op.drop_column('addresses', 'street')
    op.drop_column('addresses', 'postal_code')
    op.drop_column('addresses', 'notes')
    op.drop_column('addresses', 'country_id')
    op.drop_column('addresses', 'city')
    op.drop_column('addresses', 'area')
    op.drop_table('requests')
    op.drop_table('items')
    op.drop_table('users')
    op.drop_table('item_types')
    op.drop_table('countries')
    # ### end Alembic commands ###
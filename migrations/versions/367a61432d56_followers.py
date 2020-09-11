"""'followers'

Revision ID: 367a61432d56
Revises: 8b0c38b0cf6e
Create Date: 2020-09-07 09:43:16.286792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '367a61432d56'
down_revision = '8b0c38b0cf6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###

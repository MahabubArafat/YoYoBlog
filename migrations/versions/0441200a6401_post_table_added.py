"""post table added 

Revision ID: 0441200a6401
Revises: 14c7f0e3f26d
Create Date: 2020-08-05 11:23:33.073587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0441200a6401'
down_revision = '14c7f0e3f26d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=300), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user._id'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###

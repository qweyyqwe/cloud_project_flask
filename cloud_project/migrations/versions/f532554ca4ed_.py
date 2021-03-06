"""empty message

Revision ID: f532554ca4ed
Revises: b35dac3ca111
Create Date: 2022-04-09 17:34:36.496796

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f532554ca4ed'
down_revision = 'b35dac3ca111'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('nick_name', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('img', sa.String(length=64), nullable=True))
    op.drop_column('user', 'user_name')
    op.drop_column('user', 'profile_photo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_photo', mysql.VARCHAR(length=64), nullable=True))
    op.add_column('user', sa.Column('user_name', mysql.VARCHAR(length=32), nullable=True))
    op.drop_column('user', 'img')
    op.drop_column('user', 'nick_name')
    # ### end Alembic commands ###

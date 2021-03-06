"""empty message

Revision ID: 1218dddbe82d
Revises: 1886e7368716
Create Date: 2022-04-07 09:31:58.673093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1218dddbe82d'
down_revision = '1886e7368716'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_comment',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('course', sa.Integer(), nullable=True),
    sa.Column('to_user', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['course'], ['tb_course.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_user'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_comment')
    # ### end Alembic commands ###

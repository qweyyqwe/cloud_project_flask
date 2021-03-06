"""empty message

Revision ID: 47fdd2888adc
Revises: 1218dddbe82d
Create Date: 2022-04-07 09:47:28.165885

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '47fdd2888adc'
down_revision = '1218dddbe82d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_comments',
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
    op.drop_table('tb_comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_comment',
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.Column('update_time', mysql.DATETIME(), nullable=True),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('course', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('to_user', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('parent_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('content', mysql.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['course'], ['tb_course.id'], name='tb_comment_ibfk_1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_user'], ['user.id'], name='tb_comment_ibfk_2', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.id'], name='tb_comment_ibfk_3', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('tb_comments')
    # ### end Alembic commands ###

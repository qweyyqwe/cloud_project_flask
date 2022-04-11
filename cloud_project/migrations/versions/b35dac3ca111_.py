"""empty message

Revision ID: b35dac3ca111
Revises: 47fdd2888adc
Create Date: 2022-04-07 18:11:13.422792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b35dac3ca111'
down_revision = '47fdd2888adc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_goods',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('course', sa.Integer(), nullable=True),
    sa.Column('goods_type', sa.String(length=24), nullable=True),
    sa.Column('title', sa.String(length=24), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=20, scale=5), nullable=True),
    sa.Column('channel_type', sa.String(length=24), nullable=True),
    sa.Column('period', sa.Integer(), nullable=True),
    sa.Column('is_launched', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['course'], ['tb_course.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('tb_usercourse',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('course', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course'], ['tb_course.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_order',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('goods', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.String(length=24), nullable=False),
    sa.Column('trade_no', sa.String(length=24), nullable=True),
    sa.Column('pay_time', sa.DateTime(), nullable=True),
    sa.Column('pay_method', sa.String(length=24), nullable=True),
    sa.Column('status', sa.String(length=8), nullable=True),
    sa.Column('total_amount', sa.DECIMAL(precision=20, scale=5), nullable=True),
    sa.Column('cur_amount', sa.DECIMAL(precision=20, scale=5), nullable=True),
    sa.Column('pay_amount', sa.DECIMAL(precision=20, scale=5), nullable=True),
    sa.Column('record', sa.String(length=24), nullable=True),
    sa.ForeignKeyConstraint(['goods'], ['tb_goods.product_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_order')
    op.drop_table('tb_usercourse')
    op.drop_table('tb_goods')
    # ### end Alembic commands ###
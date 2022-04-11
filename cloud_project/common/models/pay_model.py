"""
购买相关
"""
from common.models import db
from datetime import datetime
from common.models.user_model import UserBase, VIP
from common.models.course_model import Base, Course


"""
购买相关
"""
from common.models import db
from datetime import datetime
from common.models.user_model import UserBase
from common.models.course_model import Base, Course


class Goods(Base):
    """
    商品表
    """
    __tablename__ = 'tb_goods'

    product_id = db.Column(db.Integer, primary_key=True, doc='商品id')
    course = db.Column(db.Integer, db.ForeignKey("tb_course.id", ondelete="CASCADE"))
    goods_type = db.Column(db.String(24), doc='商品种类vip/course', default='course')
    title = db.Column(db.String(24), doc='商品名称')
    price = db.Column(db.DECIMAL(20, 5), doc='商品价格')
    channel_type = db.Column(db.String(24), doc='购买渠道', default='支付宝')
    period = db.Column(db.Integer, default=365, doc='有效期')
    is_launched = db.Column(db.Boolean, default=True)
    vip = db.Column(db.Integer, db.ForeignKey("vip.id", ondelete="CASCADE"))

    def __str__(self):
        return self.title


class Orders(Base):
    """
    订单表
    """
    __tablename__ = 'tb_order'
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), doc='下单用户')
    goods = db.Column(db.Integer, db.ForeignKey("tb_goods.product_id", ondelete="CASCADE"))
    order_id = db.Column(db.String(24), doc='订单号', primary_key=True)
    trade_no = db.Column(db.String(24), doc='支付宝订单号')
    pay_time = db.Column(db.DateTime)
    pay_method = db.Column(db.String(24), doc='支付方式', default='支付宝')
    status = db.Column(db.Integer, doc='0未支付1已支付2取消支付3支付异常', default=0)
    total_amount = db.Column(db.DECIMAL(20, 5), doc='商品总金额')
    cur_amount = db.Column(db.DECIMAL(20, 5), doc='折扣后的价格')
    pay_amount = db.Column(db.DECIMAL(20, 5), doc='支付金额')
    record = db.Column(db.String(24), doc='支付信息')

    def __str__(self):
        return self.order_id


class UserCourse(Base):
    """
    用户购买的课程
    """

    __tablename__ = 'tb_usercourse'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    course = db.Column(db.Integer, db.ForeignKey("tb_course.id", ondelete="CASCADE"))


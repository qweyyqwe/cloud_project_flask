# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : pay_resoures.py
# @Software: PyCharm


"""
钉钉登录原理


支付相关
支付宝支付流程
1、前端携带课程id，获取商品信息。后端获取到用户购买的商品信息


用户购买商品-----》后端验证商品信息、验证支付价格，生成订单号，生成支付支付链接-----》前端打开链接，展示支付页面-----》例如：扫码支付-----》
回调接口，携带code码-----》前端发起请求，携带code码----》后端验证用户是否支付。。。。。

"""

import datetime
import logging
import random
import traceback

from alipay import AliPay
from flask import Blueprint, g
from flask_restful import Resource, Api, reqparse

from common.models import rds, db
from common.models.pay_model import Orders
from common.utils.custom_output_json import custom_output_json
from common.utils.qlogin_decorator import login_required

pay_bp = Blueprint('pay_bp', __name__, url_prefix='/pay')
api = Api(pay_bp)

# path = os.getcwd()
# print(path)

# app_private_key_string = open("cloud_project/pays/public.txt").read()
# alipay_public_key_string = open("cloud_project/pays/private.txt").read()


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


class CreateOrder(Resource):
    """
    生成订单
    """

    @login_required
    def get(self):
        # 判断是否登录
        user_id = g.user_id
        order = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(user_id) + str(random.randint(1000, 9999)))
        rds.set("order" + str(user_id), order)
        return {'order': order}


class Alipay(Resource):
    """
    支付
    """

    @login_required
    def get(self):
        # 获取订单号
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('order')
        parser.add_argument('price')
        args = parser.parse_args()
        order = args.get('order')
        price = args.get('price')

        order = Orders.query.get(order)
        total_amount = order.total_amount
        # # if abs(price - total_amount) >= 10:
        # #     return {'message': '订单异常'}, 500
        #
        # alipay = AliPay(
        #     appid="2016102400753303",
        #     app_notify_url=None,  # 默认回调url
        #     app_private_key_string=app_private_key_string,
        #     alipay_public_key_string=alipay_public_key_string,
        #     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     sign_type="RSA2",  # RSA 或者 RSA2
        #     debug=True  # 默认False
        # )
        #
        # # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # try:
        #     order_str = alipay.api_alipay_trade_page_pay(
        #         subject="实验楼消费",
        #         notify_url=None,
        #         out_trade_no=order,  # 订单号
        #         total_amount=price,  # 订单价格
        #         return_url="http://127.0.0.1:8080/vip"
        #     )
        #     print('zzzzzzzzzz', order_str)
        #     request_url = 'https://openapi.alipaydev.com/gateway.do?' + order_str
        #     print('zzzzzzzzzzzzzzzzzz', request_url)
        #     result = {
        #         "code": 200,
        #         "message": "请求成功，跳转支付页面",
        #         "data": request_url
        #     }
        #
        #     return result
        # except:
        #     error = traceback.format_exc()
        #     logging.error('Alipay error:{}'.format(error))
        #     return {'message': error}, 500

        result = {
            "code": 200,
            "message": "请求成功，跳转支付页面",
            "data": 'http://127.0.0.1:8080/'
        }

    # 订单入库
    def post(self):
        resp = {}
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('order')
        parser.add_argument('price')
        parser.add_argument('record')
        args = parser.parse_args()
        order = args.get('order')
        price = args.get('price')
        record = args.get('record')
        print(order, price, record)

        # 判断用户是否登录及本地订单与传过来的订单是否一致
        logging.info('Alipay get user_id:{}  order:{}  price:{}  record:{}'.format(user_id, order, price, record))
        rds_order = rds.get("order" + str(user_id))
        rds_order = rds_order.decode()
        print("111111111111111", rds_order)
        if not user_id or order != rds_order:
            resp["code"] = 405
            resp["message"] = "请求失败，请刷新页面重试"
            return resp
        order_id = Orders.query.filter_by(order_id=order).first()
        if order_id:
            resp["code"] = 405
            resp["message"] = "该订单已存在，请确认后再次提交"
            return resp
        # 将订单入库
        price = int(price) * 100  # 将价格单位改为分
        goods = 1
        order = Orders(user=user_id, order_id=order, total_amount=price, record=record, goods=goods)
        db.session.add(order)
        db.session.commit()
        resp["code"] = 200
        resp["message"] = "订单已生成，请继续完成支付"
        return resp


class GetAlipay(Resource):
    """
    查询支付接口
    查询该订单是否完成支付
    """

    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order')
        args = parser.parse_args()
        order = args.get('order')
        # 获取token中的uid
        user_id = g.user_id

        order = Orders.query.filter_by(order_id=order, user=int(user_id)).first()
        if not order or order.status != 0:
            return {"code": 405, "message": "订单不存在或已付款，请刷新后查看"}
        # TODO 调用支付宝接口，获取支付信息
        # TODO 1、支付金额（主要） 2、支付时间
        # TODO 判断实际的支付金额是否与订单中的支付金额一致。允许的差值范围1分钱
        order.status = 1
        # TODO 区分是购买的课程还是vip等级
        goods_id = order.goods
        goods = Goods.query.get(goods_id)
        course_id = goods.course
        user_course = UserCourse(user=user_id, course=course_id)
        db.session.add(user_course)
        db.session.commit()
        return {"code": 200, "message": "恭喜您，购买成功"}


class AliPayBack(Resource):
    """
    支付宝支付回调
    """

    @login_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('trade_no')
        parser.add_argument('order_id')
        parser.add_argument('timestamp')
        parser.add_argument('pay_amount')
        args = parser.parse_args()
        trade_no = args.get('trade_no')
        timestamp = args.get('timestamp')
        order_id = args.get('order_id')
        pay_amount = args.get('pay_amount')
        # 获取token中的uid
        user_id = g.user_id
        order = Orders.query.get(order_id=order_id)
        if not order:
            return {"code": 500, "message": "购买失败"}

        # TODO 验证当前支付是否成功、是否合法

        order.trade_no = trade_no
        order.pay_time = timestamp
        order.status = 1
        db.session.commit()
        # TODO 购买课程或者vip等级
        # # 3. 处理用户购买课程流程
        # # 3.1 给 UserCourse 表增加 购买课程
        # # goods = order.goods
        # user = order.user
        # course = order.goods.course
        # UserCourse.objects.create(user=user,course=course)
        return {"code": 200, "message": "购买成功"}


api.add_resource(GetAlipay, '/get_alipay', endpoint='get_alipay')
api.add_resource(AliPayBack, '/alipay_back', endpoint='alipay_back')
api.add_resource(CreateOrder, '/create_order', endpoint='create_order')
api.add_resource(Alipay, '/alipay', endpoint='alipay')

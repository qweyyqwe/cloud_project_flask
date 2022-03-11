# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : book_resoures.py
# @Software: PyCharm

import redis
import traceback
# 创建蓝图
from datetime import datetime, timedelta

from flask import Blueprint, g, request
from flask_restful import Api, Resource, reqparse, marshal, fields
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from common.models.model import User, Channel
from common.models import db, rds
from common.utils.pyjwt import generate_jwt, _generate_token, refresh_token
from common.utils.qlogin_decorator import login_required

book_bp = Blueprint('book', __name__)
api = Api(book_bp)


class BookResource(Resource):
    def get(self):
        return 'ok'


class SMSVerificationCodeResource(Resource):
    """
    验证码发送视图
    """

    def post(self):
        # 获取用户手机号码
        req = reqparse.RequestParser()
        req.add_argument('mobile')
        args = req.parse_args()
        mobile = args['mobile']
        print('mobile>>>', mobile)
        # 给用户发送手机号码: ali-sdk
        client = AcsClient(
            "LTAI4G7FrRj37co9gGDFRfbX",
            "9NxJUZdNj7B21dJ627WuKYqc4MEuiV",
            "cn-hangzhou"
        )
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', "17679962330")
        request.add_query_param('SignName', "云资讯")
        request.add_query_param('TemplateCode', "SMS_211497619")
        response = client.do_action(request)
        # print('response>>>>>', response)
        # print(str(response, encoding='utf-8'))
        # 连接Redis, 存储验证码
        rds = redis.Redis()
        rds.setex(mobile, 200, '123456')
        return {'message': 'ok', 'data': {'mobile': mobile}}


user_fields = {
    'uid': fields.Integer,
    'account': fields.String,
    'password': fields.String,
    'mobile': fields.String,
    'introduction': fields.String,
    'email': fields.String
}


class AuthorizationResource(Resource):
    """
    注册账号
    """

    def post(self):
        parser = reqparse.RequestParser()
        args_list = ['account', 'password', 'mobile', 'is_media']
        for args in args_list:
            parser.add_argument(args, required=True)
        args = parser.parse_args()
        account = args.get('account')
        password = args.get('password')
        mobile = args.get('mobile')
        is_media = args.get('is_media')
        # # 验证码
        # code = args.get('code')
        # print('验证码是————', code)
        # print(type(code))

        # 验证手机号是否已使用
        number = User.query.filter_by(mobile=mobile).count()
        if number >= 1:
            return {'code': 405, 'result': '该手机已绑定用户，请更换手机号'}

        # 验证用户是否已经注册
        user = User.query.filter_by(account=account).first()
        if user:
            return {'code': 405, 'result': '该用户已存在'}

        # # 添加手机验证码
        # rds_code = rds.get(mobile)
        # if not rds_code:
        #     return {'code': 406, 'result': '验证码过期，请重新发送验证'}
        # # 从redis中获取的验证码为字节类型，需要转换成字符类型
        # rds_code = rds_code.decode()
        # # 校验手机验证码
        # if rds_code != code:
        #     return {'code': 403, 'result': '验证码错误'}

        # 通过验证，注册用户
        user = User(account=account, password=password, mobile=mobile)
        user.last_login = datetime.now()
        db.session.add(user)
        db.session.commit()
        return marshal(user, user_fields)


class Login(Resource):
    """
    登录
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account')
        parser.add_argument('password')
        args = parser.parse_args()
        account = args.get('account')
        password = args.get('password')

        # 判断用户账号密码是否正确
        user = User.query.filter_by(account=account, password=password).first()
        if not user:
            return {'code': 406, 'result': '用户名或密码错误'}
        user.last_login = datetime.now()
        db.session.commit()
        # expiry = datetime.utcnow() + timedelta(60 * 10)
        # token = generate_jwt({'account': account}, expiry)

        token, refresh_token = _generate_token(account, user.uid)
        return {'code': 200, 'result': {'token': token, 'refresh_token': refresh_token}}


class DayToken(Resource):
    """
    15天之后的token}
    """

    def put(self):
        return refresh_token()


class GetUserInfo(Resource):
    """
    获取用户基本信息
    """

    @login_required
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('account')
        # args = parser.parse_args()
        # account = args.get('account')
        account = g.account
        print(">>>>", account)
        try:
            user = User.query.filter_by(account=account).first()
        except Exception as e:
            error = traceback.format_exc()
            print(">>>", error)
            return {'code': 500, 'result': 'GetUserInfo error'}
        return marshal(user, user_fields)
        # if user:
        #     return marshal(user, user_fields)
        # return {'code': 200, 'result': 'Not find user'}


'''
class GetUserInfo(Resource):
    """
    获取用户基本信息
    """
    @login_required
    def get(self):
        account = g.account
        print('account', account)
        try:
            user = User.query.filter_by(account=account).first()
        except:
            error = traceback.format_exc()
            print('GetUserResource error:{}'.format(error))
            return {'code': 500, 'result': 'GetUserResource error'}
        if user:
            return marshal(user, user_fields)
        return {'code': 200, 'result': 'Not find user'}
'''


class PutUserInfo(Resource):
    """
    修改用户信息
    """

    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        args_list = ['user_name', 'password', 'email', 'introduction', 'mobile']
        for args in args_list:
            # 添加校验参数
            parser.add_argument(args)
        parser.add_argument('profile_photo', location='files')
        args = parser.parse_args()
        account = g.account
        user = User.query.filter_by(account=account)
        if not user:
            return {'code': 500, 'result': '服务器异常'}
        data = {}
        # 循环参数列表
        for arg in args_list:
            # 获取对应参数的value
            arg_value = args.get(arg)
            # 判断值是否为空，是否需要去更新
            if arg_value:
                # 将需要更新的字段生成字典
                data.update({arg: arg_value})
        user.update(data)
        db.session.commit()
        return marshal(user.first(), user_fields)


class GetUsers(Resource):
    """
    获取所有用户信息
    """

    def get(self):
        user = User.query.all()
        return marshal(user, user_fields, envelope='data')


mredis = redis.Redis(host='192.168.86.207', port=6379, password=None)
api.add_resourse(AuthorizationResource, '/register_user', endpoint='register_user')
api.add_resourse(Login, '/login', endpoint='login')
api.add_resourse(SMSVerificationCodeResource, '/sms/codes/', endpoint='codes')
api.add_resourse(BookResource, '/index', endpoint='book')
api.add_resourse(GetUserInfo, '/getuserinfo', endpoint='getuserinfo')
api.add_resourse(PutUserInfo, '/putuserinfo', endpoint='putuserinfo')
api.add_resourse(DayToken, '/daytoken', endpoint='daytoken')
api.add_resourse(GetUsers, '/getusersall', endpoint='getuserall')

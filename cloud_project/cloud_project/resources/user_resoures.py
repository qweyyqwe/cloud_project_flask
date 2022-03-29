# @Email   : mat_wu@163.com
# @File    : book_resoures.py
# @Software: PyCharm

import logging
import traceback
# 创建蓝图
from datetime import datetime

import redis
from flask import Blueprint, g
from flask_restful import Api, Resource, reqparse, marshal, fields

from common.models import db
from common.models.model import User
from common.models.user_model import UserBase
from common.utils.pyjwt import _generate_token, refresh_token
from common.utils.qlogin_decorator import login_required

users_bp = Blueprint('users', __name__)
api = Api(users_bp)


class BookResource(Resource):
    def get(self):
        return 'ok'


user_fields = {
    'uid': fields.Integer,
    'account': fields.String,
    'password': fields.String,
    'mobile': fields.String,
    'introduction': fields.String,
    'email': fields.String,
    # 'is_verified': fields.Boolean,
    'certificate': fields.String,
}


class AuthorizationResource(Resource):
    """
    注册账号
    """

    def post(self):
        parser = reqparse.RequestParser()
        args_list = ['account', 'password', 'mobile', 'email', 'introduction', 'certificate']
        for args in args_list:
            parser.add_argument(args, required=True)
        args = parser.parse_args()
        account = args.get('account')
        password = args.get('password')
        mobile = args.get('mobile')
        email = args.get('email')
        # is_verified = args.get('is_verified')
        introduction = args.get('introduction')
        certificate = args.get('certificate')

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
        # 验证邮箱是否存在
        emails = User.query.filter_by(email=email).first()
        if emails:
            return {'code': 405, 'result': '该邮箱已存在'}

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
        user = User(account=account, password=password, mobile=mobile, email=email, introduction=introduction, certificate=certificate)
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
        # 最后一次登录时间
        user.last_login = datetime.now()

        # 第一种
        user_id = user.uid
        db.session.commit()
        token, refresh_token = _generate_token(account, user_id)
        return {'code': 200, 'result': {'token': token, 'refresh_token': refresh_token}}

        # # 第二种
        # db.session.commit()
        # # expiry = datetime.utcnow() + timedelta(60 * 10)
        # # token = generate_jwt({'account': account}, expiry)
        # token, refresh_token = _generate_token(account, user.uid)
        # return {'code': 200, 'result': {'token': token, 'refresh_token': refresh_token}}


class DayToken(Resource):
    """
    15天之后的token}
    """

    def post(self):
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
            logging.error('AddCourseType is error:{}'.format(error))
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
        args_list = ['user_name', 'password', 'email', 'introduction', 'mobile', 'certificate']
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


course_resource_fields = {
    'id': fields.Integer,
    'account': fields.String,
    'phone': fields.String,
    'password': fields.String,
    'user_name': fields.String,
    'address': fields.String,
}


class CourseResource(Resource):
    """
    注册账号
    """

    def post(self):
        parser = reqparse.RequestParser()
        args_list = ['account', 'password', 'phone', 'user_name', 'address']
        for args in args_list:
            parser.add_argument(args, required=True)
        args = parser.parse_args()
        account = args.get('account')
        password = args.get('password')
        phone = args.get('phone')
        user_name = args.get('user_name')
        address = args.get('address')
        number = UserBase.query.filter_by(phone=phone).count()
        if number >= 1:
            return {'code': 405, 'result': '该手机已绑定用户，请更换手机号'}
        # 验证用户是否已经注册
        user = UserBase.query.filter_by(account=account).first()
        if user:
            return {'code': 405, 'result': '该用户已存在'}
        user = UserBase(account=account, password=password, phone=phone, user_name=user_name, address=address)
        user.last_login = datetime.now()
        db.session.add(user)
        db.session.commit()
        return marshal(user, course_resource_fields)


class CourseLogin(Resource):
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
        user = UserBase.query.filter_by(account=account, password=password).first()
        if not user:
            return {'code': 406, 'result': '用户名或密码错误'}
        # 最后一次登录时间
        user.last_login = datetime.now()
        user_id = user.uid
        db.session.commit()
        token, refresh_token = _generate_token(account, user_id)
        return {'code': 200, 'result': {'token': token, 'refresh_token': refresh_token}}


mredis = redis.Redis(host='192.168.86.207', port=6379, password=None)
api.add_resource(AuthorizationResource, '/register_user', endpoint='register_user')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(BookResource, '/index', endpoint='book')
api.add_resource(GetUserInfo, '/getuserinfo', endpoint='getuserinfo')
api.add_resource(PutUserInfo, '/putuserinfo', endpoint='putuserinfo')
api.add_resource(DayToken, '/daytoken', endpoint='daytoken')
api.add_resource(GetUsers, '/getusersall', endpoint='getuserall')
api.add_resource(CourseResource, '/course_resource', endpoint='course_resource')
api.add_resource(CourseLogin, '/course_login', endpoint='course_login')

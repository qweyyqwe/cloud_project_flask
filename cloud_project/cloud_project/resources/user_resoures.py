# @Email   : mat_wu@163.com
# @File    : book_resoures.py
# @Software: PyCharm

import logging
import random
import traceback
# 创建蓝图
from datetime import datetime
from io import BytesIO

import redis
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from flask import Blueprint, g, make_response
from flask_restful import Api, Resource, reqparse, marshal, fields
from sqlalchemy import or_, and_

from celery_task.main import add
from common.models import db, rds
from common.models.model import User
from common.models.user_model import UserBase
from common.utils.pyjwt import _generate_token, refresh_token
from common.utils.qlogin_decorator import login_required
from common.utils.verify import generate_code

users_bp = Blueprint('users', __name__)
api = Api(users_bp)


class BookResource(Resource):
    def get(self):
        return 'ok'


user_fields = {
    'uid': fields.Integer,
    'account': fields.String,
    'password': fields.String,
    'phone': fields.String,
    'introduction': fields.String,
    'email': fields.String,
    # 'is_verified': fields.Boolean,
    'certificate': fields.String,
}


class SMSVerificationCodeResource(Resource):
    """
    验证码发送视图
    """

    def get(self):
        # 获取用户手机号码
        req = reqparse.RequestParser()
        req.add_argument('mobile')
        args = req.parse_args()
        print(args)
        mobile = args['mobile']
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
        print(str(response, encoding='utf-8'))
        # 连接Redis, 存储验证码
        rds.setex(mobile, 200, '852963')
        return {'message': 'ok', 'data': {'mobile': mobile}}


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
        user = User(account=account, password=password, mobile=mobile, email=email, introduction=introduction,
                    certificate=certificate)
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

    # @login_required
    def get(self):
        '''
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

        parser = reqparse.RequestParser()
        parser.add_argument('uid')
        args = parser.parse_args()
        uid = args.get('uid')
        if uid:
            user = UserBase.query.get(uid)
            return {'code': 200, 'data': {
                'img': user.img, 'username': user.account
            }}


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
        '''
        # try:
        #     parser = reqparse.RequestParser()
        #     args_list = ['account', 'password', 'phone', 'code', 'uuid']
        #     for args in args_list:
        #         parser.add_argument(args, required=True)
        #     args = parser.parse_args()
        #     account = args.get('account')
        #     password = args.get('password')
        #     phone = args.get('phone')
        #     # 图片验证码
        #     code = args.get('code')
        #     # 图片的uuid
        #     uuid = args.get('uuid')
        #
        #     """
        #     # 短信验证码
        #     msg_code = args.get('msg_code')
        #     # 注册账号时的短信验证
        #     if not msg_code:
        #         return {'code': 406, 'message': '短信验证码错误'}
        #     # 从redis中取出短信验证码
        #     real_msg_code = rds.get(phone)
        #     # 判断是否存在  不存在
        #     if not real_msg_code:
        #         return {'code': 407, 'message': '短信验证码过期'}
        #     real_msg_code = real_msg_code.decode()
        #
        #     # 进行验证是否一致
        #     if real_msg_code != msg_code:
        #         return {'code': 406, 'message': '短信验证码错误'}
        #
        #     if not all([account, password, phone, code]):
        #         return {'message': 'params is error', 'code': 400}
        #     """
        #
        #     # 图形验证码
        #     real_code = rds.get(uuid)
        #     if not real_code:
        #         return {'code': 407, 'message': '验证码过期'}
        #     real_code = real_code.decode()
        #     real_code = real_code.lower()
        #     code = code.lower()
        #     if real_code != code:
        #         return {'code': 406, 'message': '验证码错误'}
        #
        #     # 验证手机号是否使用
        #     number = UserBase.query.filter_by(phone=phone).count()
        #     if number >= 1:
        #         return {'code': 405, 'result': '该手机已绑定用户，请更换手机号'}
        #     # 验证用户是否已经注册
        #     user = UserBase.query.filter_by(account=account).first()
        #     if user:
        #         return {'code': 405, 'result': '该用户已存在'}
        #     user = UserBase(account=account, password=password, phone=phone)
        #     user.last_login = datetime.now()
        #     db.session.add(user)
        #     db.session.commit()
        #     return marshal(user, course_resource_fields)
        # except:
        #     error = traceback.format_exc()
        #     logging.error('register_user error:{}'.format(error))

        '''
        parser = reqparse.RequestParser()
        parser.add_argument('account')
        parser.add_argument('password')
        parser.add_argument('phone')
        parser.add_argument('code')
        parser.add_argument('uuid')
        args = parser.parse_args()
        account = args.get('account')
        password = args.get('password')
        phone = args.get('phone')
        code = args.get('code')
        uuid = args.get('uuid')
        print(account, password, phone, code, uuid)
        if not all([account, password, phone, code]):
            return {'message': 'fail', 'code': 407, 'data': 'account or password is null'}
        user = UserBase.query.filter_by(account=account).first()
        if user:
            return {'message': 'fail', 'code': 401, 'data': 'Mysql have user'}

        # 验证手机号是否已使用
        number = UserBase.query.filter_by(phone=phone).count()
        if number >= 1:
            return {'code': 405, 'result': '该手机已绑定用户，请更换手机号'}
        # 验证用户是否已经注册
        user = UserBase.query.filter_by(account=account).first()
        if user:
            return {'code': 405, 'result': '该用户已存在'}
        # 图形验证码
        real_code = rds.get(uuid)
        if not real_code:
            return {'code': 407, 'message': '验证码过期'}
        real_code = real_code.decode()
        real_code = real_code.lower()
        code = code.lower()
        print('11111111', real_code, code)
        if real_code != code:
            return {'code': 406, 'message': '验证码错误'}

        # redis_cli = redis.Redis(db=0)
        # data = redis_cli.get("phone_%s" % phone)
        # print('????', data)
        # if data.decode() != code:
        #     return {'message': 'fail', 'code': 500, 'data': 'code no'}
        user = UserBase(account=account, password=password, phone=phone)
        db.session.add(user)
        db.session.commit()
        return {'message': 'ok', 'code': 201, 'date': marshal(user, course_resource_fields)}


class CourseLogin(Resource):
    """
    登录
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account')
        # parser.add_argument('phone')
        parser.add_argument('password')
        # 图片验证码
        # parser.add_argument('code')
        # 图片的uuid
        # parser.add_argument('uuid')
        args = parser.parse_args()
        account = args.get('account')
        password = args.get('password')
        # phone = args.get('phone')
        # code = args.get('code')
        # uuid = args.get('uuid')
        # 不能為空
        if not all([account, password]):
            return {'message': 'params is error', 'code': 400}

        """
        user = UserBase.query.filter(and_(or_(UserBase.account == account, UserBase.phone == account),
                                          UserBase.password == args.get('password'))).first()
        if user:
            user_id = user.id
            # 生成 token
            token, refresh_token = _generate_token(user_id)
            return {'code': 200, 'data': {
                'token': token, 'refresh_token': refresh_token,
                'username': user.account, 'uid': user.id,
            }, 'message': 'login ok ok ok'}
        else:
            return {'code': 400, 'message': 'The account or password is incorrect'}
        """

        # # TODO 通过前端的uuid来刷新的
        # # 獲取真正图形验证码
        # # 獲取前端的uuid
        # real_code = rds.get(uuid)
        # if not real_code:
        #     return {'code': 407, 'message': '验证码过期'}
        # real_code = real_code.decode()
        # real_code = real_code.lower()
        # code = code.lower()
        # if real_code != code:
        #     return {'code': 407, "message": '错误'}

        """
        # 注册短信验证码
        if not msg_code:
            return {'message': '过期', 'code': 407}
        # 从redis中取出短信验证码
        msg_code = rds.get(phone)
        # 判断是否存在  不存在
        if not msg_code:
            return {'code': 407, 'message': '短信验证码过期'}
        msg_code = msg_code.decode()
        # 验证码是否一致
        if msg_code != msg_code:
            return {'message': '错误', 'code': 407}
        # 验证手机号是否已使用
        number = UserBase.query.filter_by(phone=phone).count()
        if number >= 1:
            code = args.get('code')
            uuid = args.get('uuid')

            real_code = rds.get(uuid)
            if not real_code:
                return {'code': 407, 'message': '验证码过期'}
            real_code = real_code.decode()
            if real_code != code:
                return {'code': 406, 'message': '验证码错误'}
        """

        # # 判断用户账号密码是否正确
        user = UserBase.query.filter_by(account=account, password=password).first()
        if not user:
            return {'code': 406, 'result': '用户名或密码错误'}
        # 最后一次登录时间
        user.last_login = datetime.now()
        user_id = user.id
        db.session.commit()
        token, refresh_token = _generate_token(account, user_id)

        return {'code': 200, 'data': {
            'token': token, 'refresh_token': refresh_token,
            'username': user.account, 'uid': user.id,
        }, 'message': 'ok ok ok'}


class VerificationCode(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('uuid')
            args = parser.parse_args()
            uuid = args.get('uuid')
            print('uuid>>>>>>', uuid)

            text, image = generate_code()
            rds.setex(uuid, 60 * 5, text)
            out = BytesIO()
            image.save(out, 'png')
            out.seek(0)
            resp = make_response(out.read())
            resp.content_type = 'image/png'
            return resp
        except:
            error = traceback.format_exc()
            logging.error('code image error{}'.format(error))
            return 'fail'


class MessageCode(Resource):
    """
    短信验证码
    """

    def get(self):
        # 生成验证码
        code = str(random.randint(100000, 999999))
        mobile = '13782032526'
        # 发送验证码
        # res = phone_code(mobile, code)
        res = add.delay(10, 10)
        print('>>>>', res)
        # 把短信验证码放入redis
        rds.setex(mobile, 60, code)
        return {'message': '发送验证码成功', 'code': 200}


class UserBaseInfo(Resource):
    """
    获取用户信息
    """

    # @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        uid = args.get('id')
        if uid:
            user = UserBase.query.get(uid)
            return {'code': 200, 'data': {'username': user.account}}


mredis = redis.Redis(host='192.168.86.207', port=6379, password=None)
api.add_resource(AuthorizationResource, '/register_user', endpoint='register_user')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(BookResource, '/index', endpoint='book')
api.add_resource(GetUserInfo, '/getuserinfo', endpoint='getuserinfo')
api.add_resource(PutUserInfo, '/putuserinfo', endpoint='putuserinfo')
api.add_resource(DayToken, '/daytoken', endpoint='daytoken')
api.add_resource(GetUsers, '/getusersall', endpoint='getuserall')

api.add_resource(CourseResource, '/course_register', endpoint='user/register_user')
api.add_resource(CourseLogin, '/course_login', endpoint='user/login')
api.add_resource(VerificationCode, '/verification_code', endpoint='user/code')
api.add_resource(MessageCode, '/sendalysms', endpoint='sendalysms')
api.add_resource(UserBaseInfo, '/user_info', endpoint='user_info')

# @Email   : mat_wu@163.com
# @File    : qlogin_decorator.py
# @Software: PyCharm


from flask import g, request
from functools import wraps
from common.models import rds


def login_required(func):
    # 强制登录的装饰器
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(g, 'account'):
            return {'code': 400, 'message': 'Invalid token not account'}
        if g.account is not None:
            return func(*args, **kwargs)
        return {'code': 401, 'message': 'Invalid token'}
    return wrapper


def check_code(func):
    """
    图形验证码
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        code = request.form.get('code')
        uuid = request.form.get('uuid')
        real_code = rds.get(uuid)
        if not real_code:
            return {'code': 407, 'message': '验证码过期'}
        real_code = real_code.decode()
        real_code = real_code.lower()
        code = code.lower()
        if real_code != code:
            return {'code': 406, 'message': '验证码错误'}
        return func(*args, **kwargs)
        # return {'code': 401, 'message': 'Invalid token account is none'}

    return wrapper

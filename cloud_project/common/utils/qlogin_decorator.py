# @Email   : mat_wu@163.com
# @File    : qlogin_decorator.py
# @Software: PyCharm


from flask import g
from functools import wraps


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

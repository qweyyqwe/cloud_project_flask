# # -*- coding: utf-8 -*-
# # @Time    : 2021/11/22
# # @Author  : 杨玉磊
# # @Email   : mat_wu@163.com
# # @File    : qlogin_decorator.py
# # @Software: PyCharm


from flask import g
from functools import wraps


def login_required(func):
    # 强制登录的装饰器
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user.id is not None:
            return func(*args, **kwargs)
        return {'code': 401, 'msg': 'Invalid token'}

    return wrapper

# # (1).函数名的打印
# def func():
#     """
#     func 的说明
#     """
#     # print('func执行了')
#
#
# print('函数名为: {}'.format(func.__name__, func.__doc__))  # func

# # (2).被装饰函数的函数名
# def outer(func):
#     def wrapper(*args, **kwargs):
#         print('代码块1')
#         func()
#         print('代码块2')
#     return wrapper
# @outer
# def func():
#     print('func执行了')
# print('函数名为: {}'.format(func.__name__))  # wrapper
#
# # (3).修复
# from functools import wraps
#
#
# def outer(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print('代码块1')
#         func()
#         print('代码块2')
#     return wrapper
#
#
# @outer
# def func():
#     print('func执行了')
#
#
# func()
# print('函数名为: {}'.format(func.__name__))

# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : pyjwt.py
# @Software: PyCharm
import jwt
import traceback

from flask import current_app


def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 盐
    :return: token
    """
    _payload = {
        # 过期时间
        'exp': expiry
    }
    _payload.update(payload)
    # 字典没返回值
    if not secret:
        secret = current_app.config['JWT_SECRET']
    token = jwt.encode(_payload, secret, algorithm='HS256')
    # pyjwt  1.7.1版本  返回的是字节
    # 更新2.3.0返回str
    return token

'''
from datetime import datetime, timedelta

import jwt
import traceback

from flask import current_app


def generate_jwt(payload, expiry, secret=None, refresh=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 盐
    :return: token
    """
    _payload = {
        # 过期时间
        'exp': expiry
    }
    _payload.update(payload)
    # 字典没返回值
    if not secret:
        secret = current_app.config['JWT_SECRET']
    if refresh:
        payload = {'exp': datetime.utcnow() + timedelta(days=15)}
        payload.update(payload)
        token = jwt.encode(payload, secret, algorithm='HS256')
        refresh_token = 'Bearer' + token
    token = 'Bearer' + jwt.encode(_payload, secret, algorithm='HS256')
    # pyjwt  1.7.1版本  返回的是字节
    # 更新2.3.0返回str
    return refresh_token, token
'''


def verify_jwt(token, secret=None):
    """
    校验jwt
    :param token: token值
    :param secret: 盐
    :return: payload 载荷
    """
    if not secret:
        secret = current_app.config['JWT_SECRET']

    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    except:
        error = traceback.format_exc()
        print('error', error)
        payload = None
    return payload

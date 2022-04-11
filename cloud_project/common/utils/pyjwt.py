# @Email   : mat_wu@163.com
# @File    : pyjwt.py
# @Software: PyCharm

import traceback
from datetime import datetime, timedelta

import jwt
from flask import current_app, g


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
        # print('error', error)
        payload = None
    return payload


def _generate_token(user_id, refresh=True):
    """
    生成token
    :param user_id:
    :return:
    """
    # 获取盐
    secret = current_app.config.get('JWT_SECRET')
    # 定义过期时间        2小时
    expiry = datetime.utcnow() + timedelta(hours=2)
    # 生成Token
    token = 'Bearer ' + generate_jwt({'user_id': user_id}, expiry, secret)

    if refresh:
        expiry = datetime.utcnow() + timedelta(days=15)
        # is_refresh作为更新token的信号/
        refresh_token = 'Bearer ' + generate_jwt({'user_id': user_id, 'is_refresh': True}, expiry,
                                                 secret)
    else:
        refresh_token = None
    return token, refresh_token


def refresh_token():
    """
    刷新token
    :return:
    """
    if g.account is not None and g.is_refresh is True:
        token, refresh_token = _generate_token(g.account, g.user_id, refresh=False)
        return {'message': 'ok', 'data': {'token': token}}
    else:
        return {'message': 'Invalid refresh token', 'code': 403}


def check_rds_token():
    pass

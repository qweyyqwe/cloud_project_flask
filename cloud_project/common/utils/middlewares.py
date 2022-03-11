# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : middlewares.py
# @Software: PyCharm


# encoding: utf-8
from flask import request, g
from common.utils.pyjwt import verify_jwt


def jwt_authentication():
    print("jwt_authentication()")
    g.account = None
    g.user_id = None
    g.is_refresh = False
    # 获取请求头中的token
    token = request.headers.get('Authorization')
    if token is not None and token.startswith('Bearer '):
        token = token[7:]

        # 验证token
        payload = verify_jwt(token)


        if payload is not None:
            # 保存到g对象中
            g.account = payload.get('account')
            g.user_id = payload.get('user_id')
            g.is_refresh = payload.get('is_refresh', False)


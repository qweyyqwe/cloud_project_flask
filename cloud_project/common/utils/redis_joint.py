# encoding: utf-8
from flask import request, g
from common.utils.pyjwt import verify_jwt


def jwt_authentication():
    print("jwt_authentication()")
    g.account = None
    # 获取请求头中的token
    g.is_refresh = False
    g.user_id = None
    token = request.headers.get('Authorization')
    if token is not None and token.startswith('Bearer '):
        token = token[7:]
        print(token)
        # 验证token
        payload = verify_jwt(token)

        if payload is not None:
            # 保存到g对象中
            g.user_id = payload.get('account')
            g.is_refresh = payload.get('is_refresh')
            g.user_id = payload.get('user_id')

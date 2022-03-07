# import sys
# sys.path.append('../../')

# from common.settings.settings import Fik
# from cloud_project.resources import create_book_app
#
# app = create_book_app(Fik)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

import time

from datetime import timedelta, datetime
from flask import Flask, request, jsonify
from common.utils.pyjwt import generate_jwt, verify_jwt

from common.settings.settings import Fik
from cloud_project.resources import create_book_app
app = create_book_app(Fik)


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    pwd = request.form.get("password")
    payload = {
        'name': username
    }
    expiry = datetime.utcnow() + timedelta(seconds=5000)
    token = generate_jwt(payload, expiry)
    if pwd and token and username:
        return {'code': 200, 'result': {'username': username, 'token': token}}
    else:
        return {'code': 500, 'msg': '错误'}


@app.route('/get_token', methods=['GET'])
def index():
    token = request.form.get('token')
    payload = verify_jwt(token)
    print(time.time())
    if payload:
        return {'code': 200, 'result': payload}
    else:
        return 'Token not working'

 #将时间戳转换为标准时间格式
def timestamp_to_fomat(timestamp=None,format='%Y-%m-%d %H:%M:%S'):
    #默认返回当前格式化好的时间
    #传入时间戳的话，把时间戳转换成格式化好的时间，返回
    if timestamp:
        time_tuple = time.localtime(timestamp)
        res = time.strftime(format,time_tuple)
    else:
        res = time.strftime(format)#默认读取当前时间
    return res
print(timestamp_to_fomat())



# asc-507


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)

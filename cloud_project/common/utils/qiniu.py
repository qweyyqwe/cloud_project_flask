# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : qiniu.py
# @Software: PyCharm


from qiniu import Auth
AK = 't3cMfIhCo01zE0bBrsZZN7t6qB4neh8HW_QnOamy'
SK = '97pMyQwZ6A3M_gZa2TKvf_ekuvyli9EPudfxRYKx'

# 要上传的空间
bucket_name = 'p8admin-yang'


def get_qiniu_token():
    # 构建鉴权对象
    q = Auth(AK, SK)
    # 生成上传  Token  可以指定过期时间
    token = q.upload_token(bucket_name)
    return token

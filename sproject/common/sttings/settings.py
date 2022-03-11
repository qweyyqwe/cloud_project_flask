# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : settings.py
# @Software: PyCharm

# from flask import Flask

class Fik(object):
    # mysql://账户名@host:port/库名
    SQLALCHEMY_DATABASE_URI = 'mysql://root:9@127.0.0.1:3306/project'
    # 异常开启或警报   关闭警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 显示执行sql过程
    SQLALCHEMY_ECHO = True

# app = Flask(__name__)
# # 加载数据配置
# app.config.from_object(Fik)

# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : __init__.py.py
# @Software: PyCharm


# 3.创建工厂函数: 在stusys下的__init__.py下创建工程函数
from flask import Flask
from common.models import db
from project.resources.resoures import stubp
from flask_restful import Api

# 工厂函数
def creat_flask_app(config):
    # 实例化app实例
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config)
    # db对象绑定app
    db.init_app(app)

    # z注册蓝图...
    app.register_blueprint(stubp)

    # 创建api...
    api = Api(app)

    return app
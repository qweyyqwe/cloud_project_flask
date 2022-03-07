# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : __init__.py.py
# @Software: PyCharm

# 建立工厂函数
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from common.models import db
from cloud_project.resources.book_resoures import book_bp
from common.utils.middlewares import jwt_authentication

def create_book_app(config):
    # 实例化app
    app = Flask(__name__)
    # 加载对象配置
    app.config.from_object(config)

    app.before_request(jwt_authentication)
    # db绑定对象app
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(book_bp)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    api =Api(app)
    return app

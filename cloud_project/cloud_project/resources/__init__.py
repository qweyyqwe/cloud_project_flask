# @Email   : mat_wu@163.com
# @File    : __init__.py.py
# @Software: PyCharm

# 建立工厂函数
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from common.models import db
from cloud_project.resources.user_resoures import users_bp
from cloud_project.resources.book_resoures import books_bp
from cloud_project.resources.channel_resoures import channel_bp
from cloud_project.resources.course_resoures import course_bp
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
    app.register_blueprint(users_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(channel_bp)
    app.register_blueprint(course_bp)
    CORS(app, resources={r"/*/*": {"origins": "*"}})
    # CORS(app, supports_credentials=True)

    """
    app.scheduler = BackgroundScheduler(executors=executors)
    # 每隔一分钟执行一次
    app.scheduler.add_job(update_recommend_list, trigger='interval', hours=1, args=[cache, app])
    app.scheduler.add_job(update_recommend_list, trigger='date', args=[cache, app])
    # app.scheduler.add_job(update_recommend_list, trigger='interval', hours=1, args=[cache, app])
    # app.scheduler.add_job(update_recommend_list, trigger='date', args=[cache, app])
    # app.scheduler.add_job(func=cron_test, trigger='interval', seconds=10)
    # app.scheduler.add_job(func=GetUserAttentionNew, trigger='date')
    app.scheduler.start()
    """

    api = Api(app)
    return app

# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : user_model.py
# @Software: PyCharm


from datetime import datetime
from common.models import db


class UserBase(db.Model):
    """
    用户基本信息
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, doc='用户ID')
    account = db.Column(db.String(32), doc='账号')
    phone = db.Column(db.String(16), doc='手机号')
    password = db.Column(db.String(32), doc='密码')
    nick_name = db.Column(db.String(32), doc='昵称')
    img = db.Column(db.String(64), doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    address = db.Column(db.String(128), doc='地址')
    vip = db.Column(db.Integer, db.ForeignKey("vip.id", ondelete="CASCADE"))
    vip_expiration = db.Column(db.DateTime, doc='vip到期时间')
    is_superuser = db.Column(db.Integer, default=0, doc='0普通用户1管理员2超级管理员')
    register_time = db.Column(db.DateTime, doc='注册时间', default=datetime.now)


class VIP(db.Model):
    """
    vip 表
    """
    __tablename__ = 'vip'

    id = db.Column(db.Integer, primary_key=True, doc='vip ID')
    title = db.Column(db.String(32), doc='名称')
    level = db.Column(db.String(32), doc='等级')
    desc = db.Column(db.String(256), doc='描述信息')
    period = db.Column(db.Integer, default=365, doc='vip的有效期')


class OauthUser(db.Model):
    """
    第三方登录表(微信登录/qq登录/微博登录)
    """
    __tablename__ = 'oauth_user'
    id = db.Column(db.Integer, primary_key=True, doc='oauth_user id')
    image = db.Column(db.String(64), doc='头像')
    uid = db.Column(db.String(512), doc='第三方登录的id')
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    oauth_type = db.Column(db.String(128), doc='第三方登录类型')
    @classmethod
    def is_bind_user(cls, uid, oauth_type):
        """
        是否绑定用户
        """
        oauth = OauthUser.query.filter_by(uid=uid, oauth_type=oauth_type).first()
        if oauth:
            return True
        return False

# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : book_model.py
# @Software: PyCharm


from datetime import datetime
from common.models import db


class Books(db.Model):
    """
    用户基本信息
    书籍
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, doc='books_id')
    title = db.Column(db.String(32))
    pub_date = db.Column(db.DateTime, default=datetime.now)
    read = db.Column(db.Integer)
    comment = db.Column(db.Integer)
    is_delete = db.Column(db.Integer, default=0, doc='1表示删除0表示未删除')

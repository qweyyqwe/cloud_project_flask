# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : commit_model.py
# @Software: PyCharm


from common.models import db
from common.models.course_model import Base, Course


class Comments(Base):
    """
    评论表
    """
    __tablename__ = 'tb_comments'

    id = db.Column(db.Integer, primary_key=True, doc='评论id')
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), doc='评论者')
    course = db.Column(db.Integer, db.ForeignKey("tb_course.id", ondelete="CASCADE"), doc='评论的课程')
    to_user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), doc='TODO')
    status = db.Column(db.Integer, doc='评论状态（合法0/违规1)', default=0)
    parent_id = db.Column(db.Integer, doc='楼中楼的回复')
    content = db.Column(db.Text, doc='评论内容')

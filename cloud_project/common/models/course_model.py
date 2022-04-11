# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : vip.py
# @Software: PyCharm


from common.models import db
from datetime import datetime
from common.models.user_model import UserBase


class Base(db.Model):
    __abstract__ = True
    create_time = db.Column(db.DateTime, default=datetime.now, doc='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, doc='更新时间')
    user_id = db.Column(db.Integer, doc='课程相关添加人')


class CourseType(db.Model):
    """
    课程类别
    """

    id = db.Column(db.Integer, primary_key=True, doc='课程类型id')
    title = db.Column(db.String(16), doc='课程类别')
    sequence = db.Column(db.Integer, doc='展示顺序', default=10)

    __tablename__ = 'tb_course_type'

    def __str__(self):
        return self.title


class CourseTag(Base):
    """
    课程标签
    """
    __tablename__ = 'tb_course_tag'

    id = db.Column(db.Integer, primary_key=True, doc='课程标签id')
    title = db.Column(db.String(16), doc='课程类别')
    sequence = db.Column(db.Integer, doc='展示顺序', default=10)
    course = db.relationship('Course', secondary='course_tag', backref=db.backref('tags'))

    def __str__(self):
        return self.title


class Course(Base):
    """
    课程表
    """

    __tablename__ = 'tb_course'

    STATUS = (
        ('0', '即将上线'),
        ('1', '已上线'),
        ('2', '已下线'),
    )
    id = db.Column(db.Integer, primary_key=True, doc='课程id')
    title = db.Column(db.String(24), doc='课程名称')
    desc = db.Column(db.String(256), doc='课程藐视')
    img_path = db.Column(db.String(256), doc='课程logo地址')
    course_type = db.Column(db.Integer, db.ForeignKey("tb_course_type.id", ondelete="CASCADE"))
    # course_tag = models.ManyToManyField('course_tag', verbose_name='课程标签')
    status = db.Column(db.String(8), doc='课程logo地址', default='已上线')
    follower = db.Column(db.Integer, default=0, doc='关注人数')
    learner = db.Column(db.Integer, default=0, doc='学习人数')
    chapters = db.relationship('Chapters', backref='tb_course')

    def __str__(self):
        return self.title


class CourseTitle(Base):
    """
    课程表与课程标签   的中间件
    """

    __tablename__ = 'course_tag'
    course_id = db.Column(db.Integer, db.ForeignKey("tb_course.id"), primary_key=True, doc='课程id')
    tag_id = db.Column(db.Integer, db.ForeignKey("tb_course_tag.id"), primary_key=True, doc='标签id')
    is_delete = db.Column(db.Boolean, doc='状态(0存在对应关系;1不存在对应关系)')


class Chapters(Base):
    """
    章节目录
    """
    __tablename__ = 'tb_chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(24), doc='章标题')
    serial_num = db.Column(db.Integer, doc='章序号')
    course = db.Column(db.Integer, db.ForeignKey("tb_course.id", ondelete="CASCADE"), doc='课程')
    sections = db.relationship('Sections', backref='tb_chapters')

    def __str__(self):
        return self.title


class Sections(Base):
    """
    标题目录
    """
    __tablename__ = 'tb_sections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(24), doc='章标题')
    serial_num = db.Column(db.Integer, doc='章序号')
    chapters = db.Column(db.Integer, db.ForeignKey("tb_chapters.id", ondelete="CASCADE"), doc='课程')
    learn_time = db.Column(db.Integer, doc='学习小时', default=1)
    content = db.Column(db.Text, doc='学习内容')
    video = db.Column(db.String(256), doc='学习视频')
    seq_num = db.Column(db.Integer, doc='序号', default=1)
    like_count = db.Column(db.Integer, doc='点赞次数', default=0)

    def __str__(self):
        return self.title

# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : models.py
# @Software: PyCharm

# 模块  表
from common.models import db


# 专业表
class Sub(db.Model):
    __tablename__ = 'sub'
    id = db.Column(db.Integer, primary_key=True, doc='专业ID', autoincrement=True)
    name = db.Column(db.String(32), doc='专业名称')
    stu = db.relationship('Stu', uselist=False)


# 学生表
class Stu(db.Model):
    __tablename__ = 'stu'
    stu_id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc='学生ID')
    name = db.Column(db.String(32), doc='学生姓名')
    age = db.Column(db.Integer, doc='学生年龄')
    snum = db.Column(db.Integer, unique=True, doc='学生学号')
    sub_id = db.Column(db.Integer, db.ForeignKey('sub.id'), doc='专业外键')

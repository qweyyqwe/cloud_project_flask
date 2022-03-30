# -*- coding: utf-8 -*-
# @Time    : 2021/11/22
# @File    : course_resoures.py
# @Software: PyCharm

import logging
import traceback

from flask import Blueprint, g
from flask_restful import Api, Resource, reqparse, marshal, fields

from common.models import db, cache
from common.models.course_model import CourseType, CourseTag, Course
from common.models.user_model import UserBase
from common.utils.custom_output_json import custom_output_json
from common.utils.qlogin_decorator import login_required

course_bp = Blueprint('course', __name__)
api = Api(course_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


course_type_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'sequence': fields.Integer,
}


class AddCourseType(Resource):
    """
    添加课程类别
    要强制登录，有权限？，是否存在？，参数合法？，成功
    """

    @login_required
    def post(self):
        user_id = g.user_id
        user = UserBase.query.get(user_id)  # 获取用户ID
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('sequence', type=int)
        args = parser.parse_args()
        title = args.get('title')
        sequence = args.get('sequence')
        if len(title) > 16:
            msg = 'Title is too large!'
            logging.error('AddCourseType is error:{}'.format(msg))
            return {'message': msg, 'code': 500}
        num = CourseType.query.filter_by(title=title).count()   # 是否有该课程
        if num >= 1:
            msg = 'This type is exist!'
            logging.error('AddCourseType is error:{}'.format(msg))
            return {'message': msg, 'code': 500}
        course = CourseType(title=title, sequence=sequence)
        db.session.add(course)
        db.session.commit()
        return marshal(course, course_type_fields)


class PutCourseType(Resource):
    """
    修改课程类型  # TODO
    要登录，通过类型ID进行修改
    """

    @login_required
    def post(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('title')
        parser.add_argument('sequence', type=int)
        args = parser.parse_args()
        id = args.get('id')
        title = args.get('title')
        sequence = args.get('sequence')
        print(">>>>>>>>>", title)
        try:
            data = {}
            if title:
                data.update({'title': title})
            course_type = CourseType.query.filter_by(id=id)

            # 判断是否有这个课程类别
            if not course_type.first():
                return {'message': 'Not find news', 'code': 407}
            # 判断用户是否是自己  否则没权限
            if course_type.first().user.id != user_id:
                return {'message': 'Not Permission', 'code': 407}
            course_type.update(data)
            db.session.commit()
            return {'message': 'ok', 'code': 200, 'data': marshal(course_type, course_type_fields)}
        except:
            error = traceback.format_exc()
            logging.error('update_recommend_list error:{}'.format(error))


class DelCourseType(Resource):
    """
    删除课程类型
    登录，通过类型ID删除，权限，存在
    """
    @login_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        id = args.get('id')
        book = CourseType.query.get(id)
        # TODO 一直可以删除
        if not book:
            return {'message': 'course_type is not exist!', 'code': 405}
        book.is_delete = 1
        db.session.commit()
        return marshal(book, course_type_fields)


tag_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'sequence': fields.Integer,
}


class CourseTagMethods(Resource):
    """
    课程标签的增，删，改，操作
    """

    def post(self):
        """
        添加课程标签
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('sequence')
        args = parser.parse_args()
        title = args.get('title')
        sequence = args.get('sequence')
        tag = CourseTag(title=title, sequence=sequence)
        db.session.add(tag)
        db.session.commit()
        return marshal(tag, tag_fields)


    def put(self):
        """
        修改课程标签
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('id')
        parser.add_argument('sequence')
        args = parser.parse_args()
        title = args.get('title')
        id = args.get('id')
        sequence = args.get('sequence')
        tag = CourseTag.query.get(id)
        if not tag:
            return {'message': 'tag is not exist!', 'code': 405}
        tag.title = title
        db.session.commit()
        return marshal(tag, tag_fields)


    def delete(self):
        """
        删除课程标签
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        id = args.get('id')
        tag = CourseTag.query.get(id)
        if not tag:
            return {'message': 'tag is not exist!', 'code': 405}
        tag.is_delete = 1
        db.session.commit()
        return marshal(tag, tag_fields)


course_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'desc': fields.String,
    'status': fields.String,
    'follower': fields.Integer,
    'learner': fields.Integer,
}


class CourseMethods(Resource):
    """
    课程的增，删，改，操作
    """

    def post(self):
        """
        添加课程标签
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('desc')
        parser.add_argument('status')
        parser.add_argument('follower')
        parser.add_argument('learner')
        args = parser.parse_args()
        title = args.get('title')
        desc = args.get('desc')
        status = args.get('status')
        follower = args.get('follower')
        learner = args.get('learner')
        course = Course(title=title, desc=desc, status=status, follower=follower, learner=learner)
        db.session.add(course)
        db.session.commit()
        return marshal(course, course_fields)


    def put(self):
        """
        修改课程
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('id')
        args = parser.parse_args()
        title = args.get('title')
        id = args.get('id')
        course = CourseTag.query.get(id)
        if not course:
            return {'message': 'tag is not exist!', 'code': 405}
        course.title = title
        db.session.commit()
        return marshal(course, course_fields)


    def delete(self):
        """
        删除课程
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        id = args.get('id')
        course = CourseTag.query.get(id)
        if not course:
            return {'message': 'tag is not exist!', 'code': 405}
        course.is_delete = 1
        db.session.commit()
        return marshal(course, course_fields)


api.add_resource(AddCourseType, '/add_course_type', endpoint='add_course_type')
api.add_resource(PutCourseType, '/put_course_type', endpoint='put_course_type')
api.add_resource(DelCourseType, '/del_course_type', endpoint='del_course_type')
api.add_resource(CourseTagMethods, '/course_tag_methods', endpoint='course_tag_methods')
api.add_resource(CourseMethods, '/course_methods', endpoint='course_methods')

# -*- coding: utf-8 -*-
# @Time    : 2021/11/22
# @File    : course_resoures.py
# @Software: PyCharm

import logging
import os
import traceback

from flask import Blueprint, g, request, send_from_directory
from flask_restful import Api, Resource, reqparse, marshal, fields
from werkzeug.utils import secure_filename

from common.models import db
from common.models.course_model import CourseType, CourseTag, CourseTitle, Course, Chapters, Sections
from common.models.user_model import UserBase
from common.utils.custom_output_json import custom_output_json
from common.utils.qiniu import get_qiniu_token
from common.utils.qlogin_decorator import login_required

course_bp = Blueprint('course', __name__)
api = Api(course_bp)

UPLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'images')


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


course_type_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'sequence': fields.Integer,
}

chapters_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'serial_num': fields.Integer,
}

course_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'desc': fields.String,
    'img_path': fields.String,
    'status': fields.String,
    'follower': fields.Integer,
    'learner': fields.Integer,
}

sections_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'serial_num': fields.Integer,
    'learn_time': fields.DateTime,
    'content': fields.String,
    'video': fields.String,
    'seq_num': fields.Integer,
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
        num = CourseType.query.filter_by(title=title).count()  # 是否有该课程
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


class GetTagList(Resource):
    """
    展示所有标签
    """

    def get(self):
        tag = CourseTag.query.all()
        return {'message': 'ok', 'data': marshal(tag, tag_fields)}


class GetCourseList(Resource):
    """
    展示所有课程
    """

    def get(self):
        course = Course.query.all()
        return {'message': 'ok', 'data': marshal(course, course_fields)}


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
        parser.add_argument('img_path')
        parser.add_argument('status')
        parser.add_argument('follower')
        parser.add_argument('learner')
        args = parser.parse_args()
        title = args.get('title')
        desc = args.get('desc')
        img_path = args.get('img_path')
        status = args.get('status')
        follower = args.get('follower')
        learner = args.get('learner')
        course = Course(title=title, desc=desc, img_path=img_path, status=status, follower=follower, learner=learner)
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


class UploadVideo(Resource):
    """
    上传视频
    """

    def post(self):
        try:

            f = request.files['file']
            # f = request.form.get('file')
            print("fff11111111111", f.filename)
            # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            upload_path = os.path.join(UPLOAD_PATH, secure_filename(f.filename))
            f.save(upload_path)
            video_path = os.path.join('images', f.filename)
            return {'message': 'ok', 'code': 200, 'data': {'upload_path': video_path}}
        except:
            error = traceback.format_exc()
            logging.error('UploadVideo error:{}'.format(error))
            return {'message': error, 'code': 500}


class GetUploadFile(Resource):
    def get(self, filename):
        return send_from_directory(UPLOAD_PATH, filename)


class AddChapters(Resource):
    """
    添加章节目录
    """

    @login_required
    def post(self):
        user_id = g.user_id
        print(type(user_id))
        user = UserBase.query.get(user_id)
        # 是否有添加的权限（默认超级管理员可以添加）
        if user.is_superuser != 2:
            msg = 'Not permission!'
            logging.error('AddCourseType is error:{}'.format(msg))
            return {'message': msg, 'code': 500}
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('course_id', required=True)
        parser.add_argument('serial_num', default=1)
        args = parser.parse_args()
        title = args.get('title')
        course_id = args.get('course_id')
        serial_num = args.get('serial_num')
        # 判断当前course_id是否存在
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'not find course', 'code': 407}
        chapters_num = Chapters.query.filter_by(title=title, course=course_id).count()
        if chapters_num >= 1:
            return {'message': '该文章已存在', 'code': 408}
        chapters = Chapters(title=title, course=course_id, serial_num=serial_num, user_id=user_id)
        db.session.add(chapters)
        db.session.commit()
        return marshal(chapters, chapters_fields)


class AddSections(Resource):
    """
    添加章节
    """

    @login_required
    def post(self):
        user_id = g.user_id
        user = UserBase.query.get(user_id)
        # 是否有添加的权限（默认超级管理员可以添加）
        if user.is_superuser != 2:
            msg = 'Not permission!'
            logging.error('AddSections is error:{}'.format(msg))
            return {'message': msg, 'code': 500}
        parser = reqparse.RequestParser()
        parser.add_argument('chapters_id', required=True)
        parser.add_argument('title', required=True)
        parser.add_argument('serial_num', required=True)
        parser.add_argument('learn_time', default=1)
        parser.add_argument('content')
        parser.add_argument('video')
        parser.add_argument('seq_num', default=1)
        parser.add_argument('like_count', default=1)
        args = parser.parse_args()
        chapters_id = args.get('chapters_id')
        title = args.get('title')
        serial_num = args.get('serial_num')
        learn_time = args.get('learn_time')
        content = args.get('content')
        video = args.get('video')
        seq_num = args.get('seq_num')
        like_count = args.get('like_count')

        if len(title) >= 24:
            return {'message': '标题长度太大', 'code': 408}
        chapters = Chapters.query.get(chapters_id)
        print(type(chapters))
        if not chapters:
            return {'message': '所属章节不存在', 'code': 409}
        section = Sections.query.filter_by(title=title, chapters=chapters_id).first()
        if section:
            return {'message': '当前小节已存在', 'code': 410}
        if not all([title, serial_num, content, video, like_count]):
            return {'message': ' no is None', 'code': 406}
        sections = Sections(chapters=chapters_id, title=title, serial_num=serial_num, learn_time=learn_time, content=content, video=video,
                            seq_num=seq_num, like_count=like_count)
        db.session.add(sections)
        db.session.commit()
        return {'message': 'ok', 'code': 200}


class QiNiu(Resource):
    """
    七牛云上传图片 Token
    """

    def get(self):
        token = get_qiniu_token()
        return {'token': token}


class GetChaptersList(Resource):
    """
    展示文章
    """

    def get(self):
        chapters = Chapters.query.all()
        return {'message': 'ok', 'data': marshal(chapters, chapters_fields)}

class GetSectionsList(Resource):
    """
    展示所有节
    """

    def get(self):
        sections = Sections.query.all()
        return {'message': 'ok', 'data': marshal(sections, sections_fields)}


class GetOneInfo(Resource):
    """
    获取文章
    """

    def get(self):
        chapters = Chapters.query.all()
        return {'message': 'ok', 'data': marshal(chapters, chapters_fields)}
        

api.add_resource(AddCourseType, '/add_course_type', endpoint='add_course_type')
api.add_resource(PutCourseType, '/put_course_type', endpoint='put_course_type')
api.add_resource(DelCourseType, '/del_course_type', endpoint='del_course_type')
api.add_resource(CourseTagMethods, '/course_tag_methods', endpoint='course_tag_methods')
api.add_resource(CourseMethods, '/course_methods', endpoint='course_methods')
api.add_resource(GetTagList, '/get_tags', endpoint='get/tags')
api.add_resource(AddChapters, '/add_chapter', endpoint='course/add_chapter')
api.add_resource(UploadVideo, '/upload_video', endpoint='upload_video')
api.add_resource(GetUploadFile, '/video/<filename>', endpoint='video')
api.add_resource(GetCourseList, '/get_course_list', endpoint='get_course_list')
api.add_resource(QiNiu, '/qi_niu', endpoint='qi_niu')
api.add_resource(GetChaptersList, '/get_chapters_list', endpoint='get_chapters_list')
api.add_resource(AddSections, '/add_sections', endpoint='add_sections')
api.add_resource(GetSectionsList, '/get_sections_list', endpoint='get_sections_list')
api.add_resource(GetOneInfo, '/get_info', endpoint='get_info')

# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : comment_resoures.py
# @Software: PyCharm


"""
评论相关
"""
import logging
import traceback
from copy import deepcopy

from flask import Blueprint, g
from flask_restful import Resource, Api, reqparse, marshal, fields

from common.models import db
from common.models.comment_model import Comments
from common.models.course_model import Course
from common.models.user_model import UserBase
from common.utils.custom_output_json import custom_output_json
from common.utils.qlogin_decorator import login_required

comment_bp = Blueprint('comment_bp', __name__)
# , url_prefix='/comment'
api = Api(comment_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


comment_fields = {
    "id": fields.Integer,
    "user": fields.Integer,
    "course": fields.Integer,
    "create_time": fields.DateTime,
    "update_time": fields.DateTime,
    "content": fields.String
}


class AddComment(Resource):
    """
    添加评论
    1、获取用户id、课程id、评论内容
    2、检查课程是否存在
    3、添加评论
    """

    @login_required
    def post(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('course_id')
        parser.add_argument('content')
        args = parser.parse_args()
        course_id = args.get('course_id')
        content = args.get('content')
        # 判断课程是否存在
        try:
            course = Course.query.get(course_id)
            if not course:
                return {'message': 'course_id is error', 'code': 200}
            comment = Comments(user=user_id, course=course_id, content=content)
            db.session.add(comment)
            db.session.commit()
            return {'message': 'ok'}
        except:
            error = traceback.format_exc()
            logging.error('AddComment is error:{}'.format(error))
            return {'message': error}, 500


# class GetComment(Resource):
#     """
#     获取章节评论
#     """
#     @marshal_with(comment_fields)
#     def get(self):
#         # TODO 获取合规的评论
#         comment = Comment.query.order_by(Comment.update_time.desc()).all()
#         #  TODO 分页
#         return comment


class GetComments(Resource):
    """
    获取评论
    """

    # @login_required
    def get(self):
        # user_id = g.user_id
        parse = reqparse.RequestParser()
        parse.add_argument("course_id")
        args = parse.parse_args()
        course_id = args.get("course_id")
        print('111111111111111', course_id)
        comments = Comments.query.filter_by(course=course_id).order_by(Comments.update_time.desc()).all()
        comment_list = marshal(comments, comment_fields)
        result = []
        for comment in comment_list:
            comment.update({
                'childlist': [],
                'user_info': {
                    'username': '1'
                },
                'is_favorite': 0,
                'count': 10
            })
            childlist = deepcopy(comment)
            childlist = [childlist]
            comment.update({
                'childlist': childlist
            })
            result.append(comment)
        return result


class UpComment(Resource):
    """
        修改评论
    """

    @login_required
    def put(self):
        # 获取用户
        user_id = g.user_id
        # 获取校验的参数
        re = reqparse.RequestParser()
        re.add_argument("id")
        args = re.parse_args()
        id = args.get("id")
        user = UserBase.query.filter_by(id=user_id).first()
        # 判断当前用户是否是超级管理员
        if user.is_superuser != 2:
            return {"message": "fail", "code": 500}
        comment = Comments.query.filter_by(id=id).first()
        if not comment:
            return {"message": "comment not find", "code": 500}
        if comment.status == 1:
            return {"message": "This comment is prohibit！", "code": 500}
        comment.status = 1
        db.session.commit()
        return {"message": "ok", "code": 200}


api.add_resource(UpComment, '/up_comment', endpoint='up_comment')
api.add_resource(AddComment, '/add_comment', endpoint='add_comment')
api.add_resource(GetComments, '/get_comments', endpoint='get_comments')

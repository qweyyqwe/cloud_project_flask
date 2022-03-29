# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : book_resoures.py
# @Software: PyCharm


from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal, fields

from common.models import db
from common.models.book_model import Books

books_bp = Blueprint('books_bp', __name__)
api = Api(books_bp)

book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'pub_date': fields.DateTime,
    'read': fields.Integer,
    'comment': fields.Integer,
    'is_delete': fields.Integer,
}


class BookResource(Resource):
    """
    图书管理API
    get 获取图书
    post 添加图书
    put 修改图书信息
    delete 删除图书信息
    """

    def get(self):
        """
        获取所有的 未删除的书籍列表
        :return:
        """

        book_list = Books.query.filter_by(is_delete=0).order_by(Books.pub_date.desc()).all()

        return marshal(book_list, book_fields)

    def post(self):
        """
        添加书籍
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('read', 0)
        args = parser.parse_args()
        title = args.get('title')
        read = args.get('read')
        book = Books(title=title, read=read)
        db.session.add(book)
        db.session.commit()
        return marshal(book, book_fields)

    def put(self):
        """
        修改书籍名称
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('id')
        args = parser.parse_args()
        title = args.get('title')
        id = args.get('id')
        book = Books.query.get(id)
        if not book:
            return {'message': 'book is not exist!', 'code': 405}
        book.title = title
        db.session.commit()
        return marshal(book, book_fields)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        id = args.get('id')
        book = Books.query.get(id)
        if not book:
            return {'message': 'book is not exist!', 'code': 405}
        book.is_delete = 1
        db.session.commit()
        return marshal(book, book_fields)


api.add_resource(BookResource, '/book_resource', endpoint='book_resource')

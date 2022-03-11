# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : resoures.py
# @Software: PyCharm

# 8.创建蓝图
# 报错时告诉具体位置
import traceback

from flask import Blueprint, request
from flask_restful import Api, Resource, marshal, marshal_with, reqparse, fields

from common.models import db
from common.models.models import Stu, Sub

stubp = Blueprint('stubp', __name__)
api = Api(stubp)


class StuResource(Resource):
    def get(self):
        return "Wang Jingchao, I'm OK"


# 序列化时 一定要指定类型
sub_json = {
    "id": fields.Integer,
    "name": fields.String
}

stu_json = {
    "name": fields.String,
    "age": fields.Integer,
    "snum": fields.Integer,
    "sub_id": fields.Integer,
}


class Add_sub(Resource):
    def post(self):
        # 创建parser的对象
        parser = reqparse.RequestParser()
        # 校验参数
        parser.add_argument('name')
        # 获取参数
        args = parser.parse_args()
        name = args.get('name')
        try:
            # 方法1
            # sub = Sub(name=name)
            # 方法2
            sub = Sub()
            sub.name = name
            db.session.add(sub)
            db.session.commit()
            # 返回 sub对象  和序列化字段
            return marshal(sub, sub_json)
        except Exception as e:
            # print(e)
            error = traceback.format_exc()
            print('error>>', error)
            return 'error'


class Add_stu(Resource):
    @marshal_with(stu_json)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('age')
        parser.add_argument('snum')
        parser.add_argument('sub_id')
        args = parser.parse_args()
        stu = Stu(name=args['name'], age=args['age'], snum=args['snum'], sub_id=args['sub_id'])
        # 方法2
        # stu = Stu(name=args.get('name'))
        db.session.add(stu)
        db.session.commit()
        return stu


'''
class Put_stu(Resource):
    @marshal_with(stu_json)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('age')
        args = parser.parse_args()
        # 根据 测试 传的sub_id  改变 该学生的名字
        stu = Stu.query.filter_by(age=args['age'])
        stu.update({'name': args['name']})
        db.session.commit()
        return stu.first()
'''
'''
class Put_stu(Resource):
    @marshal_with(stu_json)
    def put(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('name')
        # parser.add_argument('age')
        #
        # args = parser.add_argument()
        name = request.form.get('name')
        age = request.form.get('age')
        print(name,age)

        stu = Stu.query.filter_by(age=age)
        stu.update({'name':name})
        db.session.commit()
        return 'ok'
'''

class Put_stu(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('age')
        args = parser.parse_args()
        age = args.get('age')
        name = args.get('name')
        print(age, name)
        stu = Stu.query.filter(Stu.age == age).update(args)
        print('stu>>>', stu)
        db.session.commit()
        return {'msg': '修改成功'}


class Del_stu(Resource):
    def __init__(self):
        # 系统为不同的数据类型提供了预定义的聚合函数
        self.reqps = reqparse.RequestParser()

    def delete(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('name')
        # args = parser.parse_args()
        # name = args.get('name')
        # Stu.query.filter_by(name=name).delete()
        # db.session.commit()
        # return "删除成功"

        self.reqps.add_argument('snum', type=int, required=True)
        args = self.reqps.parse_args()
        stu_id = args['snum']
        print('----------', stu_id)
        stu = Stu.query.filter(Stu.snum == stu_id)
        if stu:
            stu.delete()
            db.session.commit()
            return "删除成功"
        else:
            return "失败了"


class List_stu(Resource):
    @marshal_with(stu_json)
    def get(self):
        stu = Stu.query.all()
        return stu


# 通过课程查询对应下的所有学生
class Sub_list_stu(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # add_argument——通过调用给定的参数执行程序
        parser.add_argument('name')
        args = parser.parse_args()
        name = args.get('name')
        sub = Sub.query.filter_by(name=name).first()
        stus = sub.stu
        return marshal(stus, stu_json)


api.add_resourse(StuResource, '/index', endpoint="qwe")
api.add_resourse(Add_sub, '/addsub')
api.add_resourse(Add_stu, '/addstu')
api.add_resourse(Put_stu, '/putstu')
api.add_resourse(Del_stu, '/delstu')
api.add_resourse(List_stu, '/liststu')
api.add_resourse(Sub_list_stu, '/subliststu')

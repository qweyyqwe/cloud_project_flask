# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : channel_resoures.py
# @Software: PyCharm

import logging
import traceback
from datetime import datetime

import demjson
from flask import Blueprint, g, request
from flask_restful import Api, Resource, reqparse, marshal, fields, marshal_with

from common.models import db
from common.models.model import Channel, User, UserChannel, News, Collection, Comment
from common.utils.qlogin_decorator import login_required

channel_bp = Blueprint('books', __name__)

channel_json = {
    "cname": fields.String,
    "ctime": fields.String,
    "sequence": fields.String,
}

new_json = {
    'nid': fields.Integer,
    'user_id': fields.Integer,
    'channel_id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'good_count': fields.Integer,
    'ctime': fields.DateTime,
}

comment_json = {
    'cmid': fields.Integer,
    'user_id': fields.Integer,
    'article_id': fields.Integer,
    'content': fields.String,
    'parent_id': fields.Integer,

}


class AddNewsChannel(Resource):
    """
    添加频道
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cname')
        parser.add_argument('ctime')
        parser.add_argument('sequence')
        args = parser.parse_args()
        cname = args.get('cname')
        ctime = args.get('ctime')
        sequence = args.get('sequence')
        try:

            channel = Channel(cname=cname, ctime=ctime, sequence=sequence)
        except Exception as e:
            error = traceback.format_exc()
            print(error)
            return error
        db.session.add(channel)
        db.session.commit()
        return marshal(channel, channel_json)


class ChannelAll(Resource):
    """
    展示所有频道
    """

    @marshal_with(channel_json)
    def get(self):
        channel = Channel.query.all()
        return channel


class AddUser(Resource):
    """
    设置用户
    """

    # @login_required
    # def post(self):
    #     channel_json = request.get_json()
    #     print("channel_json:{}".format(channel_json))
    #     return 'ok'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('channels')
        args = parser.parse_args()
        channel_list = args.get('channels')
        channel_list = demjson.decode(channel_list)
        print("channel_list id {}".format(channel_list))
        return 'OK'


"""
传参方式
{
    "channels":[
        {"id":1,"seq":1},{"id":2,"seq":2}
    ]
}
"""


class AddChannel(Resource):
    """
    添加channel
    """

    @login_required
    def post(self):
        channel_list = request.get_json()
        channel_list = channel_list['channels']
        print("channel_list:{}".format(channel_list))
        print('>>>', channel_list)
        # user_id = g.user_id
        user = User.query.get(g.user_id)
        print('user>>>', user)
        for channel in channel_list:
            channel_id = channel['id']
            channel_obj = Channel.query.get(channel_id)
            # 说明此频道不存在  跳过
            if not channel_obj:
                continue
                # 添加关联数据
            #     channel_obj.user.append(user)
            #     db.session.add(channel_obj)
            #     user.channels.remove(channel_obj)
            # db.session.commit()
            # channels = user.channels
            channel_obj = Channel.query.get(channel_id)
            user.channels.append(channel_obj)
        db.session.commit()
        return 'ok'


class GetUserChannel(Resource):
    """
    展示UserChannel
    """

    # @login_required
    def get(self):
        user_id = g.user_id
        user = User.query.get(g.user_uid)
        print(">>>>", user)
        # 获取用户配置的频道列表
        channel_list = user.channels
        return marshal(channel_list, channel_json)


class DelChannel(Resource):
    """
    删除userchannel
    """

    @login_required
    # 要拿到用户id和频道id
    def put(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('channel_id')
        args = parser.parse_args()
        channel_id = args.get('channel_id')
        user_channel = UserChannel.query.filter_by(uid=user_id, cid=channel_id).first()
        user_channel.is_delete = 1
        db.session.commit()
        return 'put  OK'


class AddUserNews(Resource):
    """
    添加資訊
    """

    @login_required
    def post(self):
        # 实例化
        parser = reqparse.RequestParser()
        args_list = ['channel_id', 'title', 'content']
        for args in args_list:
            # 添加校验参数
            parser.add_argument(args)
        args = parser.parse_args()
        # 获取user_id 知道要查的用户
        user_id = g.user_id
        data = {'user_id': user_id}
        # 循环参数列表
        for arg in args_list:
            # 获取对应参数的value
            arg_value = args.get(arg)
            # 判断值是否为空，是否需要去更新
            if arg_value:
                # 将需要更新的字段生成字典
                data.update({arg: arg_value})
        # # 方法1
        # news = News(**data)
        news = News(user_id=user_id, channel_id=args.get('channel_id'), title=args.get('title'),
                    content=args.get('content'))
        db.session.add(news)
        db.session.commit()
        return marshal(news, new_json)


class AllUserNews(Resource):
    """
    获取对应下的资讯
    """

    @login_required
    def get(self):
        user_id = g.user_id
        news = News.query.filter_by(user_id=user_id).all()
        return {'message': 'ok', 'data': {'channels': marshal(news, new_json)}}


class GetUserAttention(Resource):
    """
    获取用户关注的文章
    """

    def _get_user_attention_news(self, user_id):
        user = User.query.get(user_id)
        channels = user.channels
        try:
            content = {}
            for channel in channels:
                news_list = channel.news
                print('channel_name:{}'.format(channel.cname))
                # 如果数据过多   取最新的20条
                content.update({channel.cname: marshal(news_list, new_json)})
                print('GetUserAttentionNew', content)
        except:
            error = traceback.format_exc()
            print('error', error)
        return content

    def get_channel_news(self):
        """
        获取所有频道的最新的一篇资讯
        :return:
        """
        channel_list = Channel.query.all()
        content = {}
        for channel in channel_list:
            news_list = channel.news
            # if如果当前频道列表文章，在去添加结果对象中
            if news_list:
                content.update({channel.cname: marshal(news_list[-1], new_json)})
            # else:
            #     continue
        return content

    def get(self):
        user_id = g.user_id
        # 如果用户登录， 获取用户关注的频道文章
        result = {}
        if user_id:
            # 获取某个用户的频道
            result = self._get_user_attention_news(user_id)
        else:
            # 获取所有频道
            result = self.get_channel_news()
        return result


class GetNewsByChannel(Resource):
    """
    获取某个频道的文章
    """

    def get(self):
        # 通过    channel_id    取得对应下的内容
        parser = reqparse.RequestParser()
        parser.add_argument('channel_id')
        args = parser.parse_args()
        channel_id = args.get('channel_id')
        # TODO 需要完善，如果channel_id 是错误的，需要怎样处理
        # 获取频道里的channel_id   .news取到资讯表对应下的文章
        news_list = Channel.query.get(channel_id).news
        print('>>>', news_list)
        # .reverse 倒序
        # news_list.reverse()
        if len(news_list) >= 20:
            news_list = news_list[0:20]
        return marshal(news_list, new_json)


class GetNewsDetail(Resource):
    """
    获取资讯的详情
    """

    def get(self):
        # 通过nid 获取该文章的详细信息
        parser = reqparse.RequestParser()
        parser.add_argument('nid')
        args = parser.parse_args()
        nid = args.get('nid')
        new = News.query.get(nid)
        # 资讯不存在的情况下
        logging.error('error')
        logging.debug('debug')
        if not new:
            return {'code': 500, 'message': 'The news is not exist!'}
        return {'code': 200, 'data': marshal(new, new_json)}


class AddCollection(Resource):
    """
    添加用户关注
    """

    @login_required
    def post(self):
        # 获取user_id用户
        user_id = g.user_id
        user = User.query.get(user_id)
        parser = reqparse.RequestParser()
        # 资讯的id
        parser.add_argument('nid')
        args = parser.parse_args()
        nid = args.get('nid')
        news = News.query.get(nid)
        # # 方法1
        # collection = Collection(user_id=user_id, news_id=nid, is_delete=0)
        # db.session.add(collection)

        # 方法2
        user.news_collections.append(news)
        db.session.add(user)

        db.session.commit()
        return {'message': 'ok'}


'''
class GetAllCollection(Resource):
    """
    获取用户收藏的资讯
    """

    @login_required
    def get(self):
        # 获取用户id
        user_id = g.user_id
        # 获取用户对象
        user = User.query.get(user_id)
        # 获取用户收藏的资讯列表
        user_new_list = user.news_collections
        # 将最新的资讯放最前  倒序
        user_new_list.reverse()
        logging.debug('user collections:{}'.format(user_new_list))
        return {'message': 'ok', 'code': 200, 'data': marshal(user_new_list, new_json)}
'''


class GetAllCollection(Resource):
    """
    分页器
    """

    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page')
        parser.add_argument('page_size')
        args = parser.parse_args()
        page = int(args.get('page', 1))
        page_size = int(args.get('page_size', 2))
        print(page)
        print(page_size)
        user_id = g.user_id
        # 获取用户对象
        user = User.query.get(user_id)
        # 获取用户收藏的资讯列表
        user_new_list = user.news_collections
        # 将最新的资讯放最前  倒序
        user_new_list.reverse()

        total = len(user_new_list)
        # 分页
        start = (page - 1) * page_size
        end = page * page_size if total > page * page_size else total
        ret = user_new_list[start: end]
        print('>>>>>', ret)
        logging.debug('user collections:{}'.format(user_new_list))
        return {'message': 'ok', 'code': 200, 'data': marshal(user_new_list, new_json), 'total': total}


class DelCollection(Resource):
    """
    取消收藏
    """

    @login_required
    def delete(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('news_id')
        args = parser.parse_args()
        news_id = args.get('news_id')
        try:
            # 通过user_id查询news_id来取消关注
            collection = Collection.query.filter_by(user_id=user_id, news_id=news_id).first()
            if collection:
                collection.is_delete = 1
                db.session.commit()
            else:
                return {'message': 'fail', 'code': 406, 'error': 'is not invalid'}
        except:
            error = traceback.format_exc()
            logging.error('DelUserCollection delete error:{}'.format(error))
            return {'message': 'fail', 'code': 500}
        return {'message': 'ok', 'code': 200}


class UpdateNewsLikeCount(Resource):
    """
    资讯的点赞数
    """

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('news_id')
        args = parser.parse_args()
        news_id = args.get('news_id')
        news = News.query.get(news_id)
        if news:
            news.good_count += 1
            db.session.commit()
        else:
            return {'message': 'fail', 'error': 'This information is off the market error', 'code': 407}
        return {'message': 'okokok', 'code': 200, 'data': marshal(news, new_json)}


class AddNewsComment(Resource):
    """
    评论资讯
    1登陆之后评论，在那个资讯下评论的

    """

    @login_required
    def post(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('article_id')
        parser.add_argument('content', required=True)
        parser.add_argument('parent_id')
        args = parser.parse_args()
        article_id = args.get('article_id')
        content = args.get('content')
        parent_id = args.get('parent_id')
        try:
            if parent_id:
                parent_comment = Comment.query.get(parent_id)
                if not parent_comment:
                    return {'message': 'Invalid parameter', 'code': 407}
            contents = Comment(user_id=user_id, article_id=article_id, content=content, parent_id=parent_id)
            db.session.add(contents)
            db.session.commit()
        except:
            error = traceback.format_exc()
            logging.error('AddNewsComment error:{}'.format(error))
            return {'message': 'fail', 'code': 507}
        return {'message': 'ok', 'code': 200, 'data': marshal(contents, comment_json)}


class GetNewsComment(Resource):
    """
    获取资讯评论
    """

    def get(self):
        # news_id = request.args.get('news_id')
        # page = int(request.args.get('page'))
        # page_size = int(request.args.get('page_size'))
        # print(type(page))

        parser = reqparse.RequestParser()
        parser.add_argument('news_id')
        parser.add_argument('page', default=1)
        parser.add_argument('page_size', default=20)
        args = parser.parse_args()
        news_id = args.get('news_id')
        page = int(args.get('page', 1))
        page_size = int(args.get('page_size', 20))

        try:
            # 获取资讯的评论（不包括评论的评论）
            comment_list = Comment.query.filter_by(article_id=news_id, parent_id=None).all()
            comment_list.reverse()
            total = len(comment_list)
            # 分页
            # 信息的起始数据位置
            start = (page - 1) * page_size
            # 信息的结束数据位置
            end = page * page_size if total > page * page_size else total
            comment_list = comment_list[start: end]
        except:
            error = traceback.format_exc()
            logging.error('GetNewsComment error:{}'.format(error))
            return {'message': 'fail', 'code': 507, 'error': 'Server is error!'}
        return {'message': 'ok', 'code': 200, 'data': marshal(comment_list, comment_json), 'count': total}


class GetCommentChild(Resource):
    """
    获取评论的评论
    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('comment_id', required=True)
        parser.add_argument('page', default=1)
        parser.add_argument('page_size', default=20)
        args = parser.parse_args()
        comment_id = args.get('comment_id')
        page = int(args.get('page', 1))
        page_size = int(args.get('page_size', 20))
        # 获取评论的评论
        # parent_id  是评论的评论的id
        comment_list = Comment.query.filter_by(parent_id=comment_id).all()
        comment_list.reverse()

        # 分页
        total = len(comment_list)
        # 信息的起始数据位置
        start = (page - 1) * page_size
        # 信息的结束数据位置
        end = page * page_size if total > page * page_size else total
        comment_list = comment_list[start: end]

        return {'message': 'ok', 'data': marshal(comment_list, comment_json)}


class DeleteNewsComment(Resource):
    """
    删除评论
    """

    @login_required
    def put(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('cmid')
        args = parser.parse_args()
        cmid = args.get('cmid')
        try:
            comment = Comment.query.filter_by(user_id=user_id, cmid=cmid).first()
            if comment:
                comment.status = 3
                db.session.commit()
        except:
            error = traceback.format_exc()
            logging.error('DeleteNewsComment delete error:{}'.format(error))
        return {'message': 'delete ok', 'code': 204}


class PublishNews(Resource):
    """
    用户发布资讯
    """

    @login_required
    def post(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('content')
        parser.add_argument('title')
        parser.add_argument('channel_id')
        args = parser.parse_args()
        content = args.get('content')
        title = args.get('title')
        channel_id = args.get('channel_id')

        try:
            if not all([content, title, channel_id]):
                return {'code': 407, 'message': 'params is invalid!'}
            channel = Channel.query.get(channel_id)
            # 验证channel_id是否合法
            if not channel:
                return {'code': 407, 'message': 'channel_id is error!'}

            # 添加资讯  status=1是状态  是待审核
            news = News(user_id=user_id, content=content, title=title, channel_id=channel_id, status=1)
            db.session.add(news)
            db.session.commit()
        except:
            error = traceback.format_exc()
            logging.error('PublishNews error:{}'.format(error))
            return {'message': 'fail', 'code': 507, 'error': 'Server is error!'}
        return {'message': 'ok', 'code': 200, 'data': marshal(news, new_json)}


class PutNews(Resource):
    """
    修改资讯
    """

    @login_required
    def put(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('nid')
        parser.add_argument('title')
        parser.add_argument('content')
        args = parser.parse_args()
        nid = args.get('nid')
        title = args.get('title')
        content = args.get('content')
        try:
            data = {}
            if title:
                data.update({'title': title})
            if content:
                data.update({'content': content})
            # 获取用户发表的资讯id
            news = News.query.filter_by(nid=nid)

            # 判断是否有这个资讯
            if not news.first():
                return {'message': 'Not find news', 'code': 407}
            # 判断用户是否是自己  否则没权限
            if news.first().user_id != user_id:
                return {'message': 'Not Permission', 'code': 407}
            news.update(data)
            db.session.commit()
        except:
            error = traceback.format_exc()
            logging.error('PublishNews error:{}'.format(error))
            return {'message': 'fail', 'code': 507, 'error': 'Server is error!'}
        return {'message': 'ok', 'code': 200}

    @login_required
    def post(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('nid')
        parser.add_argument('title')
        parser.add_argument('content')
        args = parser.parse_args()
        nid = args.get('nid')
        title = args.get('title')
        content = args.get('content')

        # 获取对象
        news = News.query.get(nid)

        # 判断是否有这篇资讯
        if not news:
            return {'message': 'Not find news', 'code': 407}
        if news.user_id != user_id:
            return {'message': 'Not permission!', 'code': 407}

        # 资讯标题以及内容不能为空
        if title:
            news.title = title
        if content:
            news.content = content
        db.session.commit()
        return {'message': 'ok', 'code': 200, 'data': marshal(news, new_json)}


class GetListNews(Resource):
    """
    获取资讯列表
    """

    @login_required
    def get(self):
        user_id = g.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('page', default=1, type=int)
        parser.add_argument('page_size', default=20, type=int)
        args = parser.parse_args()
        page = int(args.get('page'))
        page_size = int(args.get('page_size'))
        page_size = page_size if 20 > page_size > 10 else 20
        news_list = News.query.all()
        news_list.reverse()

        # 分页
        total = len(news_list)
        # 信息的起始数据位置
        start = (page - 1) * page_size
        # 信息的结束数据位置
        end = page * page_size if total > page * page_size else total
        comment_list = news_list[start: end]

        return {'message': 'ok', 'data': marshal(comment_list, new_json)}


class DelUserNews(Resource):
    """
    删除指定资讯
    """

    @login_required
    def put(self):
        # 创建请求参数解析对象
        req = reqparse.RequestParser()
        req.add_argument('article_id', type=int)
        args = req.parse_args()
        # 获取要删除的请求参数
        article_id = args['article_id']
        # 查找用户ID
        user_id = g.user_id
        # 查找用于对应的资讯中有没有要删除的那条资讯
        news = News.query.filter_by(user_id=user_id, nid=article_id)
        if news.first():
            # 如果有, 则开始逻辑删除, 将status状态改为4(删除), 并更新删除时间
            update_values = {}
            update_values['status'] = News.STATUS.DELETED
            update_values['delete_time'] = datetime.now()
            news.update(update_values)
            db.session.commit()
        else:
            return {'message': 'Invalid request param!'}, 401
        return {'message': 'ok', 'data': {'art_id': news.first().nid}}


api = Api(channel_bp)
api.add_resource(AddNewsChannel, '/addnewschannel', endpoint='add_channel')
api.add_resource(ChannelAll, '/allchannel', endpoint='all_channel')
api.add_resource(AddUser, '/adduser', endpoint='add_user')
api.add_resource(GetUserChannel, '/getuserchannel', endpoint='getuserchannel')
api.add_resource(AddChannel, '/addchannel', endpoint='addchannel')
api.add_resource(DelChannel, '/delchannel', endpoint='delchannel')
api.add_resource(AddUserNews, '/addusernews', endpoint='addusernews')
api.add_resource(AllUserNews, '/allusernews', endpoint='allusernews')
api.add_resource(GetUserAttention, '/getuserattention', endpoint='getuserattention')
api.add_resource(GetNewsByChannel, '/getnewsbychannel', endpoint='getnewsbychannel')
api.add_resource(GetNewsDetail, '/getnewsdetail', endpoint='getnewsdetail')
api.add_resource(AddCollection, '/addcollection', endpoint='addcollection')
api.add_resource(GetAllCollection, '/getallcollection', endpoint='getallcollection')
api.add_resource(DelCollection, '/delcollection', endpoint='getallcoldelcollectionlection')
api.add_resource(UpdateNewsLikeCount, '/updatenewslikecount', endpoint='updatenewslikecount')
api.add_resource(AddNewsComment, '/addnewscomment', endpoint='addnewscomment')
api.add_resource(GetNewsComment, '/get_news_comment', endpoint='get_news_comment')
api.add_resource(GetCommentChild, '/get_comment_child', endpoint='get_comment_child')
api.add_resource(DeleteNewsComment, '/deletenewscomment', endpoint='deletenewscomment')
api.add_resource(PublishNews, '/publishnews', endpoint='publishnews')
api.add_resource(PutNews, '/putnews', endpoint='putnews')
api.add_resource(GetListNews, '/getlistnews', endpoint='getlistnews')
api.add_resource(DelUserNews, '/delusernews', endpoint='delusernews')

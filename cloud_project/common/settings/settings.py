# @Email   : mat_wu@163.com
# @File    : settings.py
# @Software: PyCharm
import pickle
import redis

# 与mysql链接
class Fik(object):
    # mysql://账户名@host:port/库名
    SQLALCHEMY_DATABASE_URI = 'mysql://root:9@127.0.0.1:3306/book_project'
    # 异常开启或警报   关闭警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 显示执行sql过程
    # SQLALCHEMY_ECHO = True
    JWT_SECRET = 'LSJFLSJFLWE23O9UDFNSDF'

    """
    缓存配置
    """
    CACHE_TYPE = 'redis'  # 使用redis作为缓存
    CACHE_KEY_PREFIX = 'students_lin'  # 设置cache_key的前缀
    CACHE_REDIS_HOST = '127.0.0.1'  # redis地址
    CACHE_REDIS_PORT = '6379'  # redis端口
    # CACHE_REDIS_PASSWORD = ''  # redis密码
    CACHE_REDIS_DB = 6  # 使用哪个数据库



class Redis:
    @staticmethod
    def connect():
        r = redis.StrictRedis(host='101.42.224.35', port=6379)
        return r

    # 将内存数据二进制通过序列号转为文本流，再存入redis
    @staticmethod
    def set_data(r, key, data, ex=None):
        r.set(key, pickle.dumps(data), ex)

    # 将文本流从redis中读取并反序列化，返回返回
    @staticmethod
    def get_data(r, key):
        data = r.get(key)
        if data is None:
            return None
        return pickle.loads(data)

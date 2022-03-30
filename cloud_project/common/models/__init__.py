# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @Author  : 杨玉磊
# @Email   : mat_wu@163.com
# @File    : __init__.py.py
# @Software: PyCharm

# 创建一个对象
from flask_sqlalchemy import SQLAlchemy
from common.settings.settings import Redis
from flask_caching import Cache
db = SQLAlchemy()
rds = Redis().connect()
cache = Cache

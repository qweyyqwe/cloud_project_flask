# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : main.py
# @Software: PyCharm
import time

from celery import Celery

# 定义celery实例, 需要的参数, 1, 实例名, 2, 任务发布位置, 3, 结果保存位置
app = Celery('mycelery',
             broker='redis://:@127.0.0.1:6379/6',  # 任务存放的地方
             backend='redis://:@127.0.0.1:6379/7', )  # 结果存放的地方


@app.task(name='celery_task.main.add')
def add(x, y):
    time.sleep(10)
    return x + y

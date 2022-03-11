# encoding:utf-8

# python 内置
import sys
import os
sys.path.append('../')
# pip 第三方包

# 项目中导入
from project.resources import creat_flask_app
from common.sttings.settings import Fik



app = creat_flask_app(Fik)

# # 全局配置跨域
# from flask_cors import CORS
# cors = CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run()

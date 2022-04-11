# 数据库迁移脚本

import pymysql
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from cloud_project.main import app
from common.models.model import *
from common.models.book_model import *
from common.models.course_model import *
from common.models.user_model import *
from common.models.comment_model import *
from common.models.pay_model import *

from common.models import db

pymysql.install_as_MySQLdb()

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()

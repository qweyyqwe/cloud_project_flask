# 数据库迁移脚本

import pymysql
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from cloud_project.main import app
from common.models import db
from common.models.model import Book
from common.models.book_model import Books


pymysql.install_as_MySQLdb()

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()


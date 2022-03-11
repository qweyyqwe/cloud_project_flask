# -*- coding: utf-8 -*-


"""
数据库迁移脚本
"""
import pymysql
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from  common.models.models import Stu, Sub, db
from project.main import app

pymysql.install_as_MySQLdb()

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()


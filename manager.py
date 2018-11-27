from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
# from vjinrong.models import Bank

from vjinrong import create_app,db
from vjinrong import models


"""
manager:只是负责启动当前应用程序


"""
app = create_app("development")
manager = Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)

"""
添加一个后台管理员用户到数据库
"""
# @manager.option('-n', '--name', dest='name')
# @manager.option('-p', '--password', dest='password')
# @manager.option('-m', '--mobile', dest='mobile')
# def create_admin_user(name,password,mobile):
#
#     bank_user = Bank()
#     bank_user.name = name
#     bank_user.password = password
#     bank_user.mobile = mobile
#     bank_user.section = "达深信息科技有限公司"
#     bank_user.rank = 3
#     bank_user.rec_num = ""
#
#     # 提交数据
#     db.session.add(bank_user)
#     db.session.commit()


if __name__ == '__main__':
    print(app.url_map)
    manager.run()
# 引入flask
from flask import Flask

# 定义函数

def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    app.config.from_object('record.code.setting')
    return app

# 注册蓝图
def register_blueprint(app):
    from record.views import admin
    app.register_blueprint(admin)
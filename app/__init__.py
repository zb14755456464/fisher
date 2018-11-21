'''
    创建应用程序，并注册相关蓝图
'''
from flask import Flask
# from flask_wtf.csrf import CsrfProtect
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()



def register_web_blueprint(app):
    from app.web import web
    app.register_blueprint(web)


def create_app(config=None):
    app = Flask(__name__)

    #: load default configuration
    app.config.from_object('app.settings')
    app.config.from_object('app.secure')

    # 注册SQLAlchemy
    db.init_app(app)
    register_web_blueprint(app)

    # 注册login模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login' # 如果没登陆的话重定向到登陆页面
    login_manager.login_message = '请先登录或注册'

    # 注册mail
    mail.__init__(app)

    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    return app

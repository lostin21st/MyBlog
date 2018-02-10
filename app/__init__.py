import os
from flask_moment import Moment
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand

moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'

from .extensions import flask_admin,babel
from .models import Post, Tag
from contorllers.admin import MyView, CustomModelView, PostView,CustomFileAdmin
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    babel.init_app(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
    flask_admin.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    flask_admin.add_view(CustomModelView(Tag,db.session,category="Models"))
    flask_admin.add_view(PostView(Post,db.session,category="Models"))
    flask_admin.add_view(
        CustomFileAdmin(
            os.path.join(os.path.dirname(__file__),'static'),
            '/static',
            name='文件管理')
    )

    return app



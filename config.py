import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    "base config class"
    SECRET_KEY = 'Max'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SAVEPIC = '/home/max/Myblog/app/static/image/upload/'
    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    "development config class"
    DEBUG  = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://max:max@localhost:3306/myblog'

config = {
    'devlopment' : DevConfig,
    'default' : DevConfig
}


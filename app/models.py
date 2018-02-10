from . import db
from . import login_manager
from datetime import datetime
from markdown import markdown
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import bleach
posts_tags = db.Table('posts_tags',
                      db.Column('post_id',db.Integer,db.ForeignKey('posts.id')),
                      db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'))
                     )

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255), index=True, unique=True)
    body = db.Column(db.Text)
    create_date = db.Column(db.DateTime,default=datetime.utcnow)
    change_date = db.Column(db.DateTime,default=datetime.utcnow)
    tags = db.relationship(
        'Tag', secondary=posts_tags,backref=db.backref('posts',lazy='dynamic'),lazy='dynamic'
    )
    show_html = db.Column(db.Text)
    body_html = db.Column(db.Text)
    '''    @staticmethod
#    def on_changed_post(target,value,oldvalue,initiaor):
        allow_tags = ['p','strong','br','del','em','blockquote','h1','h2','h3',
                      'h4','h5','h6','li','span','ol','hr','a','pre','code','table',
                      'thead','tr','tbody','acronym','b','i','img']
        allow_tags = ['del','a','abbr','acronym','b','blockquote',\
                      'code','em','li','i','ol','pre','strong','ul','h1',\
                      'h2','h4','h5','h6','hr','br','h3','p','img']
        target.body_html=bleach.linkify(bleach.clean(
            markdown(value,output_form='html'),
            attributes={
                '*': ['class','id'],
                'a': ['href','rel','title','name'],
                'img': ['alt']
            },
            tags=allow_tags,strip=True)
        )
        
        target.body_html=markdown(value,output_form='html')
    '''
    @staticmethod
    def on_changed_post(target,value,oldvalue,initiaor):
        target.change_date = datetime.utcnow()
        flag = value.find('<hr>')
        if flag == -1:
            target.show_html = value
        else:
            target.show_html = value[:flag]

    def __repr__(self):
        return "<Model Post'{}'>".format(self.title)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique=True, index=True)

    def __repr__(self):
        return "<Model Tag '{}'>".format(self.name)

class AdminUser(db.Model, UserMixin):
    __tablename__ = 'AdminUser'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True, index=True)
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

db.event.listen(Post.body_html,'set',Post.on_changed_post)

import os
from app import db
from datetime import datetime
from flask import render_template, session, redirect, url_for, Response
from flask import request, g, current_app, jsonify
from . import main
from app.models import Post,Tag
from sqlalchemy import extract, func

@main.before_request
def before_request():
    g.posts_count = Post.query.count()
    g.tags_count = Tag.query.count()

@main.route('/')
def index():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(
        Post.create_date.desc()).paginate(page,per_page=current_app.config['POSTS_PER_PAGE'],
                                   error_out=False)
    posts = pagination.items
    return render_template('index.html',posts=posts,pagination=pagination)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    all_posts = Post.query.order_by(Post.create_date.desc()).all()
    index = all_posts.index(post)
    pre_post = None if index-1<0 else (
        all_posts[index-1].id,all_posts[index-1].title
    )
    next_post = (
        all_posts[index+1].id,all_posts[index+1].title
    ) if index+1 < len(all_posts) else None
    return render_template('post.html',pre_post=pre_post,next_post=next_post,post=post)

@main.route('/tags/')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html',tags=tags)

@main.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    posts = tag.posts.all()
    return render_template('tag.html',tag=tag,posts=posts)

@main.route('/archives/')
def archives():
    posts = []
    count = Post.query.count()
    page = request.args.get('page',1, type=int)
    pagination = Post.query.order_by(Post.create_date.desc()).paginate(
        page,per_page=20,
        error_out=True
    )
    archives = db.session.query(
        extract('year',Post.create_date).label('year'),
        func.count('*').label('count')
    ).group_by('year').all()
    for archive in archives:
        per_posts = pagination.query.filter(
            extract('year',Post.create_date) == archive[0]).all()
        if per_posts:
            posts.append((archive[0],per_posts))
    return render_template('archives.html',count=count,posts=posts,pagination=pagination)

@main.route('/upload/', methods=['POST'])
def upload():
    file=request.files.get('editormd-image-file')
    if not file:
        res={'success':0,
             'message':u'图片格式异常'
            }
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S')+ex
        file.save(os.path.join(current_app.config['SAVEPIC'],filename))
        res={
            'success':1,
            'message':u'图片上传成功',
            'url':url_for('.image',name=filename)
        }
    return jsonify(res)

@main.route('/image/<name>')
def image(name):
    with open(os.path.join(current_app.config['SAVEPIC'],name),'rb') as f:
        resp=Response(f.read(),mimetype="image/jpeg")
    return resp



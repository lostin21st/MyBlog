from flask_admin import BaseView, expose,AdminIndexView,helpers
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from app.models import Post
from flask import redirect,request,url_for
import flask_login as login
from app.main.forms import CKTextAreaField, LoginForm, Body_html
class MyView(AdminIndexView):
    @expose('/',methods=['GET','POST'])
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyView,self).index()
    @expose('/login/',methods=('GET','POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyView,self).index()
    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

class CustomModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


class PostView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    column_list = ('title','date')
    form_overrides = {'body':CKTextAreaField}
    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'
    form_columns = ('tags','title','body','body_html')

class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated



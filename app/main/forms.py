from wtforms import (
    widgets,
    StringField,
    TextField,
    TextAreaField,
    PasswordField,
    BooleanField,
    ValidationError,
    HiddenField,
    form
)
from werkzeug.security import check_password_hash
from wtforms import validators
from wtforms.validators import Required
from app.models import AdminUser
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self,field,**kwargs):
        kwargs.setdefault('id','ts')
        kwargs.setdefault('style','dispaly:none')
        return super(CKTextAreaWidget,self).__call__(field,**kwargs)


class Body_html(HiddenField):
    pass

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class LoginForm(form.Form):
    username = StringField(
        label=u'管理员账号',
        validators=[Required()]
    )
    password = PasswordField(
        label=u'密码',
        validators=[Required()])

    def validate(self):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError(u'账号不存在')
        if not check_password_hash(user.password_hash,self.password.data):
            raise validators.ValidationError(u'密码错误')
        return True
    def get_user(self):
        return AdminUser.query.filter_by(
            username=self.username.data).first()



from flask_admin import Admin
from flask_babelex import Babel
from contorllers.admin import MyView

babel = Babel()
flask_admin = Admin(
    name=u'后台管理系统',
    index_view=MyView(),
    base_template='admin/my_master.html',
)



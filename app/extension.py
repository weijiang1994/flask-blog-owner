"""
# coding:utf-8
@Time    : 2020/9/17
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : extension
@Software: PyCharm
"""
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_share import Share
from flask_moment import Moment

bootstrap = Bootstrap()
mail = Mail()
ckeditor = CKEditor()
share = Share()
moment = Moment()

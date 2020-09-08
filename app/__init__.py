"""
@Time    : 2020/1/2 13:35
@Author  : weijiang
@Site    : 
@File    : __init__.py
@Software: PyCharm
@License: (@)Copyright 2001-2019,SZ_Colibri
@Contact:weijiang@colibri.com.cn
"""
import os
import logging
import datetime
from logging.handlers import RotatingFileHandler

from flask import Flask
from .blueprint.index_bp import index_bp
from .blueprint.gallery_bp import gallery_bp
from .blueprint.work_bp import work_bp
from .blueprint.own_bp import own_bp
from .blueprint.article_detail_bp import article_detail_bp
from .blueprint.login_bp import login_bp
from .blueprint.admin_bp import admin_bp
from flask_bootstrap import Bootstrap
from .blueprint.backend.create_blog_bp import create_blog_bp
from .blueprint.backend.edit_blog_bp import edit_blog_bp
from flask_ckeditor import CKEditor
from .blueprint.category_bp import category_bp
from .blueprint.timeline_bp import timeline_bp
from .blueprint.backend.gallery.add_photo_bp import add_photo_bp
from .blueprint.backend.other.add_timeline_bp import add_timeline_bp
from .blueprint.search_blog import search_bp
from .blueprint.backend.gallery.edit_photo_bp import edit_photo_bp
from .blueprint.account_bp import account_bp
from flask_share import Share

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    CKEditor(app)
    Share(app)
    app.config['current_article_title'] = ''
    app.config['CKEDITOR_SERVE_LOCAL'] = True
    app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
    app.config['CKEDITOR_HEIGHT'] = 450
    app.config['CKEDITOR_FILE_UPLOADER'] = 'create_blog_bp.upload'
    app.config['CKEDITOR_CODE_THEME'] = 'docco'
    app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')
    app.config['SECRET_KEY'] = 'dev'
    app.config['PRE_URL'] = ''
    app.permanent_session_lifetime = datetime.timedelta(days=1)
    # app.config.from_mapping(
    #     SECRET_KEY='de'
    # )
    # if test_config is None:
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_blueprint(app)
    register_log(app)
    return app


def register_blueprint(app: Flask):
    app.register_blueprint(index_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(work_bp)
    app.register_blueprint(own_bp)
    app.register_blueprint(article_detail_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(create_blog_bp)
    app.register_blueprint(edit_blog_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(timeline_bp)
    app.register_blueprint(add_photo_bp)
    app.register_blueprint(add_timeline_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(edit_photo_bp)
    app.register_blueprint(account_bp)


def register_log(app: Flask):
    app.logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler('logs/blogin.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    # if not app.debug:
    app.logger.addHandler(file_handler)

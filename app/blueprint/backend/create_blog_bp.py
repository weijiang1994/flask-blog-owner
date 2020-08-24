"""
coding:utf-8
file: create_blog_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/3/14 22:33
@desc:
"""
import os
from ...frozen_dir import app_path
from flask import Blueprint, request, render_template, url_for, send_from_directory, current_app
from flask_ckeditor import CKEditorField, upload_fail, upload_success
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.datastructures import CombinedMultiDict
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, StringField, SelectField, TextAreaField, FileField
from ..login_bp import login_require
from ...util.common_util import get_current_time, get_uuid, create_path, CATEGORY_DIC
from ...model.db_operate import DBOperator
from ...model.blogin_model import Article, BlogType

create_blog_bp = Blueprint('create_blog_bp', __name__, url_prefix='/backend')


class PostForm(FlaskForm):
    db = DBOperator()
    ret = db.query_all(BlogType)
    choices = [(i[0], i[1].type_name) for i in zip(range(len(ret)), ret)]
    title = StringField(u'博客标题', validators=[Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': '输入您的博客标题'})
    blog_type = SelectField(label=u'博客类型',
                            choices=choices, default=0,
                            coerce=int)
    blog_level = SelectField(label=u'博客权限', choices=[(1, '公开'), (2, '私有')], validators=[DataRequired()],
                             default=1, coerce=int)
    brief_content = TextAreaField(u'博客简介', validators=[DataRequired()])
    blog_img_file = FileField(label=u'博客示例图',
                              validators=[FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                              render_kw={'value': "上传", 'class': 'btn btn-default'})
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField(u'发布博客')


@create_blog_bp.route('/createBlog', methods=['GET', 'POST'])
@login_require
def index():
    form = PostForm(CombinedMultiDict([request.form, request.files]))
    if form.validate_on_submit():
        # 获取表单中信息
        blog_title = form.title.data
        blog_type = int(form.blog_type.data)+1
        blog_level = form.blog_level.data
        blog_content = form.body.data
        current_time = get_current_time()
        brief_content = form.brief_content.data
        filename = form.blog_img_file.data.filename

        # 获取当前时间并创建博客示例图片的存储文件夹
        current_time = current_time.split(' ')[0]
        create_path(app_path() + '/image/' + current_time)
        # 将博客示例图片存储到对应的文件夹中
        form.blog_img_file.data.save(app_path() + '/image/' + current_time + '/' + filename)
        blog_img_path = '/backend/blogImg/image/' + current_time + '/' + filename
        # 博客入库操作
        db = DBOperator()
        blog_obj = Article(id=get_uuid(), title=blog_title, type=blog_type, is_private=blog_level, content=blog_content,
                           brief_content=brief_content, create_time=get_current_time(), update_time=get_current_time(),
                           read_times=0, delete_flag=0, img=blog_img_path)
        db.add_data(blog_obj)
        blog_type_count = db.update_blog_type_count(BlogType, condition=CATEGORY_DIC.get(blog_type))[0]
        blog_type_count.blog_count = int(blog_type_count.blog_count) + 1
        db.commit_data()

        return render_template('articleDetail.html', title=blog_title, create_time='发布于' + str(current_time),
                               read_times='阅读数' + str(0), article_type=CATEGORY_DIC.get(blog_type), article_content
                               =blog_content)

    return render_template('/backend/createBlog.html', form=form)


@create_blog_bp.route('/files/<filename>')
def uploaded_files(filename):
    path = current_app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@create_blog_bp.route('/blogImg/image/<path>/<filename>')
def get_blog_sample_img(path, filename):
    path = app_path() + '/image/' + path + '/'
    return send_from_directory(path, filename)


@create_blog_bp.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], f.filename))
    url = url_for('create_blog_bp.uploaded_files', filename=f.filename)
    return upload_success(url=url)

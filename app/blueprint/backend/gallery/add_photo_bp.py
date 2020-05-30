"""
coding:utf-8
file: add_photo_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/5/28 23:24
@desc:
"""
from flask import Blueprint, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.datastructures import CombinedMultiDict
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import Length

from app.frozen_dir import app_path
from app.util.common_util import get_current_time, create_path

add_photo_bp = Blueprint('add_photo_bp', __name__, url_prefix='/backend')


class AddPhotoForm(FlaskForm):
    photo_title = StringField(u'相片标题', validators=[Length(min=3, max=50, message='用户名长度必须在3到50之间')],
                              render_kw={'class': '', 'rows': 50, 'placeholder': '输入照片标题'})
    photo_desc = TextAreaField(u'相片描述', validators=[Length(min=3, max=250, message='用户名长度必须在3到250之间')])
    img_file = FileField(label=u'博客示例图',
                         validators=[FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                         render_kw={'value': "上传", 'class': 'btn btn-default'})
    view_submit = SubmitField(u'预览照片')
    submit = SubmitField(u'发布照片')


@add_photo_bp.route('/addPhoto', methods=['GET', 'POST'])
def index():
    form = AddPhotoForm(CombinedMultiDict([request.form, request.files]))
    if form.validate_on_submit():
        photo_title = form.photo_title.data
        photo_desc = form.photo_desc.data
        photo_file = form.img_file.data.filename

        current_time = get_current_time()
        current_time = current_time.split(' ')[0]
        create_path(app_path() + '/gallery/' + current_time)
        # 将博客示例图片存储到对应的文件夹中
        form.img_file.data.save(app_path() + '/gallery/' + current_time + '/' + photo_file)
        blog_img_path = '/backend/blogImg/gallery/' + current_time + '/' + photo_file

    return render_template('/backend/addPhoto.html', form=form)


@add_photo_bp.route('/blogImg/gallery/<path>/<filename>')
def get_blog_sample_img(path, filename):
    path = app_path() + '/gallery/' + path + '/'
    return send_from_directory(path, filename)

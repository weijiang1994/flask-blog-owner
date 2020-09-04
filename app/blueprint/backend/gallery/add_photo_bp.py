"""
coding:utf-8
file: add_photo_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/5/28 23:24
@desc:
"""
from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, g, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.datastructures import CombinedMultiDict
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField
from wtforms.validators import Length, DataRequired
from app.frozen_dir import app_path
from app.util.common_util import get_current_time, create_path, get_uuid
from ....model.db_operate import DBOperator
from ....model.blogin_model import Gallery, PhotoTag, Tags

add_photo_bp = Blueprint('add_photo_bp', __name__, url_prefix='/backend')


class AddPhotoForm(FlaskForm):
    # 添加相册照片前端表单
    photo_title = StringField(u'相片标题',
                              validators=[DataRequired(), Length(min=1, max=20, message='用户名长度必须在1到20之间')],
                              render_kw={'class': '', 'rows': 50, 'placeholder': '输入照片标题'})
    photo_desc = TextAreaField(u'相片描述', validators=[DataRequired(), Length(min=3, max=250, message='用户名长度必须在3到250之间')])
    img_file = FileField(label=u'博客示例图',
                         validators=[DataRequired(), FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                         render_kw={'value': "上传", 'class': 'btn btn-default'})
    photo_level = SelectField(label=u'照片权限', choices=[(1, '公开'), (2, '私有')], validators=[DataRequired()],
                              default=1, coerce=int)
    tags = StringField(u'相片标签',
                       validators=[DataRequired(), Length(min=1, max=50, message='标签长度必须在1-50之间')],
                       render_kw={'placeholder': '请输入相片标签，用空格隔开～'})
    submit = SubmitField(u'发布相片')


@add_photo_bp.route('/addPhoto', methods=['GET', 'POST'])
def index():
    """
    添加相册相片视图函数
    :return:
    """
    form = AddPhotoForm(CombinedMultiDict([request.form, request.files]))
    print('获取到了请求，请求方为:', request.method)
    print(form.validate_on_submit())
    # print(session['user_id'])
    # print(g.user)
    if form.validate_on_submit():
        print('进入了表单验证')
        photo_id = get_uuid()
        photo_title = form.photo_title.data
        photo_desc = form.photo_desc.data
        photo_filename = form.img_file.data.filename
        photo_filename = photo_id + photo_filename
        photo_level = form.photo_level.data
        current_time = get_current_time()
        current_time = current_time.split(' ')[0]
        create_path(app_path() + '/gallery/' + current_time)
        # 将图片存储到服务器对应的文件夹中
        form.img_file.data.save(app_path() + '/gallery/' + current_time + '/' + photo_filename)
        blog_img_path = '/backend/blogImg/gallery/' + current_time + '/' + photo_filename
        photo_tags = form.tags.data.split()
        db = DBOperator()
        gallery = Gallery(id=photo_id, photo_title=photo_title, photo_desc=photo_desc, photo_path=blog_img_path,
                          create_time=get_current_time(), delete_flag=0, private_flag=photo_level)
        for tag in photo_tags:
            # 1.先判断tag是否已经存在与photo_tag中，如果不存在存入，如果存在则取出tag id
            tag_from_db = db.query_tag_by_tag_name(PhotoTag, tag)
            if len(tag_from_db) >= 1:
                tag_id = tag_from_db[0].id
                photo_tag_ret = db.update_photo_count(PhotoTag, condition=tag)
                photo_tag_ret.photo_counts += 1
            else:
                db.add_data(PhotoTag(tag_name=tag, photo_counts=1, create_time=get_current_time(), delete_flag=0))
                db.commit_data()
                tag_id = db.query_tag_by_tag_name(PhotoTag, tag)[0].id
            db.add_data(Tags(tag_id=tag_id, photo_id=photo_id, create_time=get_current_time()))
        db.add_data(gallery)
        db.commit_data()
        db.clear_buffer()
        del db
        # print(session['user_id'])
        # print(g.user)
        return redirect(url_for('gallery_bp.gallery'))
    return render_template('/backend/addPhoto.html', form=form)


@add_photo_bp.route('/blogImg/gallery/<path>/<filename>')
def get_gallery_img(path, filename):
    """
    获取服务器相册照片资源
    :param path: 请求携带的path
    :param filename: 请求携带的文件名
    :return: 对应的照片文件
    """
    path = app_path() + '/gallery/' + path + '/'
    return send_from_directory(path, filename)

"""
# coding:utf-8
@Time    : 2020/9/8
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : account_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, g, request, send_from_directory, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
from ..util.common_util import get_md5, get_time_delta, generate_ver_code
from ..blueprint.login_bp import user_login_require
from ..frozen_dir import app_path
from ..model.blogin_model import Users, LoginLog, Comment, Article
from ..model.db_operate import DBOperator
from ..model.blogin_model import Notification
from app.decorators import confirm_required_2_index
from app.email import send_verify_code

account_bp = Blueprint(__name__, 'account_bp', url_prefix='/accounts')


class ProfileForm(FlaskForm):
    website = StringField(u'个人网站',
                          render_kw={'class': '', 'rows': 50, 'placeholder': '输入个人网址', 'type': 'url'})
    avatar = FileField(u'个人头像', validators=[FileAllowed(['png', 'jpg'], '只接收png和jpg图片')])
    submit = SubmitField(u'保存')
    avatar_src = ''


class ResetPwdForm(FlaskForm):
    origin_pwd = StringField('原始密码',
                             validators=[DataRequired(), Length(min=8, max=20, message='密码必须在8-20个字符之间')],
                             render_kw={'placeholder': '请输入原始密码', 'type': 'password'})
    reset_pwd = StringField('重置密码', validators=[DataRequired(), Length(min=8, max=20, message='密码必须在8-20个字符之间')],
                            render_kw={'placeholder': '请输入新的密码', 'type': 'password'})
    confirm_reset_pwd = StringField('确认密码',
                                    validators=[DataRequired(), Length(min=8, max=20, message='密码必须在8-20个字符之间')],
                                    render_kw={'placeholder': '请确认密码', 'type': 'password'})
    ver_code = StringField('验证码', validators=[DataRequired(), Length(max=6, message='请输入正确的验证码')],
                           render_kw={'placeholder': '请输入验证码'})

    submit = SubmitField('修改')


@account_bp.route('/profile/', methods=['GET', 'POST'])
@user_login_require
def account_profile():
    userid = g.normal_user
    db = DBOperator()
    usr = db.query_filter_by_id(Users, condition=userid)[0]

    # 获取用户的基本信息
    login_info = db.query_by_user_id(LoginLog, condition=userid)
    if login_info:
        login_time = login_info.login_time
    user_name = usr.username
    user_join_time = usr.create_time
    user_email = usr.email
    website = usr.website
    avatar = usr.avatar
    # 显示在资料卡上的用户信息
    usr_info = [userid, user_name, user_join_time, user_email, login_time, website, avatar]
    # 获取当前用户的通知
    notifications = db.query_notification_by_receive_id(Notification, condition=g.normal_user)
    # 获取用户动态
    moments = db.query_moments_by_crt_id(Comment, condition=g.normal_user)
    ntf_comments = []
    ntf_moments = []
    for ntf in notifications:
        comm = db.query_filter_by_id(Comment, ntf.comment_id)[0]
        create_u_info = db.query_filter_by_id(Users, ntf.create_u)[0]

        create_u_name = create_u_info.username
        create_u_avatar = create_u_info.avatar
        ntf_time = ntf.create_time
        reply_content = comm.comment_content
        article_name = db.query_filter_by_id(Article, comm.article_id)[0].title
        child_nft = [ntf.id, create_u_avatar, create_u_name, ntf_time, article_name, reply_content]
        ntf_comments.append(child_nft)

    for moment in moments:
        # 父id为空说明是顶级评论
        if moment.parent_id is None:
            # 查询评论所关联的文章
            art_title = db.query_filter_by_id(Article, condition=moment.article_id)[0].title
            delta_time = get_time_delta(moment.comment_time)
            sub = [{'parentComment': None}, moment.comment_time, moment.comment_content, art_title,
                   '/detail/article/' + art_title, delta_time]
            ntf_moments.append(sub)
        else:
            # 查询父id所关联的信息
            parent = db.query_filter_by_id(Comment, condition=moment.parent_id)[0]
            parent_usr = db.query_filter_by_id(Users, condition=parent.create_u_id)[0].username
            art_title = db.query_filter_by_id(Article, condition=moment.article_id)[0].title
            delta_time = get_time_delta(moment.comment_time)
            sub = [{'parentComment': [parent_usr, parent.comment_content]},
                   moment.comment_time, moment.comment_content, art_title, '/detail/article/' + art_title, delta_time]
            ntf_moments.append(sub)
    return render_template('accountProfile.html', user_info=usr_info, nft_counts=len(notifications),
                           ntf_conmment=ntf_comments, ntf_moments=ntf_moments)


@account_bp.route('/profile/markReaded/', methods=['POST'])
@user_login_require
def mark_all_notifications():
    db = DBOperator()
    notifications = db.query_notification_by_receive_id(Notification, condition=g.normal_user)
    for ntf in notifications:
        ntf.readed = 1
    db.commit_data()
    return ''


@account_bp.route('/profile/markOne/', methods=['POST'])
@user_login_require
def mark_one_notification():
    ntf_id = request.form.get('ntfID')
    db = DBOperator()
    ntf = db.query_filter_by_id(Notification, ntf_id)[0]
    ntf.readed = 1
    db.commit_data()
    return ''


@account_bp.route('/profile/edit/', methods=['GET', 'POST'])
@user_login_require
@confirm_required_2_index
def profile_edit():
    db = DBOperator()
    usr = db.query_filter_by_id(Users, g.normal_user)[0]
    form = ProfileForm()

    if form.validate_on_submit():
        website = form.website.data
        print('提交的website', website)
        if form.avatar.data.filename:
            filename = form.avatar.data.filename
            filename = str(g.normal_user) + filename
            form.avatar.data.save(app_path() + '/avatars/' + filename)

            usr.avatar = '/accounts/profile/avatar/avatars/' + filename
        usr.website = website
        db.commit_data()
        return redirect(url_for('app.blueprint.account_bp.account_profile'))
    form.website.data = usr.website
    form.avatar_src = usr.avatar
    return render_template('profileEdit.html', form=form)


@account_bp.route('/profile/resetPwd/', methods=['GET', 'POST'])
@user_login_require
@confirm_required_2_index
def reset_pwd():
    form = ResetPwdForm()
    if form.validate_on_submit():
        db = DBOperator()
        usr = db.query_filter_by_id(Users, condition=g.normal_user)[0]
        if usr.password != get_md5(form.origin_pwd.data):
            flash('原始密码错误,请重试~')
            return render_template('resetPwd.html', form=form)
        if form.reset_pwd.data != form.confirm_reset_pwd.data:
            flash('两次密码不一致,请重试~')
            return render_template('resetPwd.html', form=form)
        usr.password = get_md5(form.confirm_reset_pwd.data)
        db.commit_data()
        return redirect(url_for('app.blueprint.account_bp.account_profile'))
    return render_template('resetPwd.html', form=form)


@account_bp.route('/profile/avatar/<path>/<filename>')
def get_gallery_img(path, filename):
    """
    获取服务器相册照片资源
    :param path: 请求携带的path
    :param filename: 请求携带的文件名
    :return: 对应的照片文件
    """
    path = app_path() + '/' + path + '/'
    return send_from_directory(path, filename)


@account_bp.route('/ver-code/', methods=['POST'])
@user_login_require
def send_ver_code():
    user_id = g.normal_user
    db = DBOperator()
    usr = db.query_filter_by_id(Users, condition=user_id)[0]
    usr_name = usr.username
    send_verify_code(usr.email, ver_code=generate_ver_code(), username=usr_name)
    return jsonify({'tag': 1, 'info': '验证码发送成功,十分钟内有效!'})

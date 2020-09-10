"""
# coding:utf-8
@Time    : 2020/9/8
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : account_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, g, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
from ..blueprint.login_bp import user_login_require
from ..model.blogin_model import Users, LoginLog, Comment, Article
from ..model.db_operate import DBOperator
from ..model.blogin_model import Notification

account_bp = Blueprint(__name__, 'account_bp', url_prefix='/accounts')


class ProfileForm(FlaskForm):
    website = StringField(u'个人网站',
                          validators=[DataRequired(), Length(min=0, max=128, message='个人网站长度必须在0到128之间')],
                          render_kw={'class': '', 'rows': 50, 'placeholder': '输入照片标题'})
    avatar = FileField(u'个人头像',  validators=[DataRequired(), FileAllowed(['png', 'jpg'], '只接收png和jpg图片')])

    submit = SubmitField(u'保存')


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
    usr_info = [userid, user_name, user_join_time, user_email, login_time, website]
    notifications = db.query_notification_by_receive_id(Notification, condition=g.normal_user)
    ntf_comments = []
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
    return render_template('accountProfile.html', user_info=usr_info, nft_counts=len(notifications),
                           ntf_conmment=ntf_comments)


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
def mark_a_notification():
    ntf_id = request.form.get('ntfID')
    db = DBOperator()
    ntf = db.query_filter_by_id(Notification, ntf_id)[0]
    ntf.readed = 1
    db.commit_data()
    return ''


@account_bp.route('/profile/edit/', methods=['GET', 'POST'])
@user_login_require
def profile_edit():
    form = ProfileForm()
    return render_template('profileEdit.html', form=form)

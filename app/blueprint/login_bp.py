"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
import functools
from flask import Blueprint, request, render_template, redirect, url_for, session, g, flash, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from app.email import send_confirm_email
from ..util.common_util import get_md5, get_current_time, AVATARS, generate_token, validate_token, Operations
from ..model.blogin_model import Users, LoginLog
from ..model.db_operate import DBOperator
import random

login_bp = Blueprint('login_bp', __name__, url_prefix='/auth')


class RegisterForm(FlaskForm):
    email = StringField(u'E-mail',
                        render_kw={'placeholder': '请输入邮箱地址', 'autofocus': 'autofocus', 'type': 'email'},
                        validators=[DataRequired()])
    username = StringField(u'用户名', render_kw={'placeholder': '请输入用户名，长度不超过8个字符'},
                           validators=[DataRequired(), Length(min=1, max=8, message='用户名长度不能超过8个字符')])
    password = StringField(u'密码', render_kw={'placeholder': '请输入密码长度8-40个字符', 'type': 'password'},
                           validators=[DataRequired(), Length(min=8, max=40, message='密码格式不正确')])
    confirm = StringField(u'确认密码', render_kw={'placeholder': '请确认密码', 'type': 'password'},
                          validators=[DataRequired(), Length(min=8, max=40, message='密码格式不正确')])
    submit = SubmitField(u'注册', render_kw={'class': 'pull-right btn btn-outline-success rounded-1', 'type': 'submit'})


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm')
        if password != confirm_password:
            flash('两次输入的密码不一致~')
            return render_template('register.html', form=form)

        db = DBOperator()
        if db.query_user_by_email(Users, email):
            flash('该邮箱已经注册~')
            return render_template('register.html', form=form)

        if db.query_user_by_name(Users, username):
            flash('该用户名已经存在~')
            return render_template('register.html', form=form)

        user = Users(email=email, username=username, password=get_md5(password), create_time=get_current_time(),
                     delete_flag=0, avatar=AVATARS[random.randint(0, len(AVATARS)-1)])
        db.add_data(user)
        db.commit_data()
        db.clear_buffer()
        del db
        token = generate_token(user=user, operation='confirm')
        send_confirm_email(user=user, token=token)
        return redirect(url_for('login_bp.user_login'))
    return render_template('register.html', form=form)


@login_bp.route('/login/', methods=['GET', 'POST'])
def login_backend():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and get_md5(password) == 'b5b26111d157f8d1def468cb7b7214d1':
            session.clear()
            session.permanent = True
            session['user_id'] = username
            return redirect(url_for('admin_bp.index'))
        else:
            flash('用户名或密码错误')
            return render_template('loginBack.html')
    return render_template('loginBack.html')


@login_bp.route('/userLogin', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = DBOperator()
        user = db.query_user_by_name(Users, condition=username)
        if user:
            if user.password != get_md5(password):
                flash('用户名或密码错误', 'danger')
                return render_template('userLogin.html')
        else:
            flash('当前邮箱或用户名不存在', 'info')
            return render_template('userLogin.html')
        session.permanent = True
        session['normal_user'] = username
        log_login(user.id, login_ip=request.remote_addr)
        if 'auth' in current_app.config.get('PRE_URL'):
            return redirect(url_for('index_bp.index'))
        else:
            return redirect(current_app.config.get('PRE_URL') or 'index_bp.index')
    current_app.config['PRE_URL'] = request.referrer
    return render_template('userLogin.html')


def log_login(userid, login_ip):
    db = DBOperator()
    log = LoginLog(user_id=userid, login_time=get_current_time(), login_ip=login_ip)
    db.add_data(log)
    db.commit_data()


@login_bp.route('/logout')
def user_logout():
    session.clear()
    return redirect(request.referrer)


# 存储管理员用户的g.use信息
@login_bp.before_app_request
def load_log_user_id():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = '804022023@qq.com'


# 存储普通用户g.normal_user
@login_bp.before_app_request
def load_normal_user_id():
    normal_user = session.get('normal_user')
    if normal_user is None:
        g.normal_user = None
    else:
        db = DBOperator()
        user = db.query_user_by_name(Users, normal_user)
        g.normal_user = user.id
        g.normal_user_name = user.username
        g.normal_user_avatar = user.avatar
        db.clear_buffer()
        del db


# 重定向到后台登录页面
def login_require(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login_bp.login_backend'))
        return view(**kwargs)

    return wrapped_view


# 重定向到普通用户登录页面
def user_login_require(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.normal_user is None:
            return redirect(url_for('login_bp.user_login'))
        return view(**kwargs)

    return wrapped_view


@login_bp.route('/confirm/<token>')
@user_login_require
def confirm(token):
    db = DBOperator()
    user = db.query_filter_by_id(Users, condition=g.normal_user)[0]
    if validate_token(user=user, token=token, operation=Operations.CONFIRM):
        user.confirmed = 1
        db.commit_data()
        flash('恭喜你,邮箱验证成功啦!', 'success')
    else:
        flash('不是你的就别想有拥有啦!╭(╯^╰)╮  邮箱验证失败啦!', 'danger')
    return redirect(url_for('index_bp.index'))


@login_bp.route('/resend-confirm-mail')
@user_login_require
def resend_confirm_mail():
    db = DBOperator()
    user = db.query_filter_by_id(Users, condition=g.normal_user)[0]
    token = generate_token(user=user, operation=Operations.CONFIRM)
    send_confirm_email(user=user, token=token)
    flash('邮箱认证邮件发送成功，请前往邮箱查看认证!', 'success')
    return redirect(url_for('index_bp.index'))

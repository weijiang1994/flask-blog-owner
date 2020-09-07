"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
import functools
from flask import Blueprint, request, render_template, redirect, url_for, session, g, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from ..util.common_util import get_md5, get_current_time
from ..model.blogin_model import Users
from ..model.db_operate import DBOperator

login_bp = Blueprint('login_bp', __name__, url_prefix='/auth')


class RegisterForm(FlaskForm):
    email = StringField(u'E-mail',
                        render_kw={'class': 'extinput textInput form-control', 'placeholder': '请输入邮箱地址',
                                   'autofocus': 'autofocus', 'type': 'email'},
                        validators=[DataRequired()])
    username = StringField(u'用户名',
                           render_kw={'class': 'extinput textInput form-control',
                                      'placeholder': '请输入用户名，长度不超过8个字符'},
                           validators=[DataRequired(), Length(min=1, max=8)])
    password = StringField(u'密码', render_kw={'class': 'extinput textInput form-control',
                                             'placeholder': '请输入密码长度8-40个字符',
                                             'type': 'password'},
                           validators=[DataRequired(), Length(min=8, max=40, message='密码格式不正确')])
    confirm = StringField(u'确认密码', render_kw={'class': 'extinput textInput form-control',
                                              'placeholder': '请确认密码',
                                              'type': 'password'},
                          validators=[DataRequired(), Length(min=8, max=40, message='密码格式不正确')])
    submit = submit = SubmitField(u'注册', render_kw={'class': 'pull-right btn btn-outline-success rounded-1',
                                                    'type': 'submit'})


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
                     delete_flag=0)
        db.add_data(user)
        db.commit_data()
        db.clear_buffer()
        del db
        return redirect(url_for('login_bp.login'))
    return render_template('register.html', form=form)


@login_bp.route('/password/reset', methods=['GET', 'POST'])
def reset_password():
    return 'password reset'


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
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
            return render_template('login.html')

    return render_template('login.html')


@login_bp.before_app_request
def load_log_user_id():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = '804022023@qq.com'


def login_require(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login_bp.login'))
        return view(**kwargs)

    return wrapped_view

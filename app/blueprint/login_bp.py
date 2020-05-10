"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
import json
import functools
from flask import Blueprint, request, render_template, redirect, url_for, session, g, jsonify


login_bp = Blueprint('login_bp', __name__, url_prefix='/auth')


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        auth_data = json.loads(request.form.get('data'))
        username = auth_data['username']
        password = auth_data['password']
        if username == 'admin' and password == 'admin':
            session.clear()
            session['user_id'] = username
            return redirect(url_for('admin_bp.index'))
        else:
            return jsonify({'error': 1})

    return render_template('/backend/login.html')


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

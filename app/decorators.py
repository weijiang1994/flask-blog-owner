"""
# coding:utf-8
@Time    : 2020/9/17
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : decorators
@Software: PyCharm
"""
from functools import wraps

from flask import Markup, flash, url_for, redirect, g, jsonify

from app.model.blogin_model import Users
from app.model.db_operate import DBOperator


def confirm_required(view):
    @wraps(view)
    def view_in(**kwargs):
        db = DBOperator()
        usr = db.query_filter_by_id(Users, condition=g.normal_user)[0]
        if not usr.confirmed:
            message = Markup(
                '请先前往邮箱确认然后进行后续操作.'
                '没有收到邮件?'
                '<a class="alert-link" href="%s">重新发送确认邮件</a>' %
                url_for('login_bp.resend_confirm_mail'))
            return jsonify({'tag': 0, 'info': message})
            return redirect(url_for('index_bp.index'))
        return view(**kwargs)
    return view_in



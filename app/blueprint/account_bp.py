"""
# coding:utf-8
@Time    : 2020/9/8
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : account_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template
from ..blueprint.login_bp import user_login_require
account_bp = Blueprint(__name__, 'account_bp', url_prefix='/accounts')


@account_bp.route('/profile', methods=['GET', 'POST'])
@user_login_require
def account_profile():
    return render_template('accountProfile.html')

"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
from flask import Blueprint, render_template

work_bp = Blueprint('work_bp',  __name__)


@work_bp.route('/tech')
def article():
    return render_template('work.html')

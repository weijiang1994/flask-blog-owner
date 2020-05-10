"""
coding:utf-8
file: timeline_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/4/14 22:33
@desc:
"""
from flask import Blueprint, render_template


timeline_bp = Blueprint('timeline_bp', __name__)


@timeline_bp.route('/timeline')
def index():
    return render_template('timeline.html')

"""
coding:utf-8
file: add_timeline_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/6/10 23:01
@desc:
"""
from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField

add_timeline_bp = Blueprint('add_timeline_bp', __name__, url_prefix='/backend')


class TimelineForm(FlaskForm):
    timeline_title = StringField(u'名称')

@add_timeline_bp.route('/addTimeline')
def index():
    return render_template('/backend/addTimeline.html')
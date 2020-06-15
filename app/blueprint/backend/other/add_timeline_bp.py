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
from wtforms import StringField, TextAreaField, SubmitField

add_timeline_bp = Blueprint('add_timeline_bp', __name__, url_prefix='/backend')


class TimelineForm(FlaskForm):
    timeline_title = StringField(u'名称')
    timeline_content = TextAreaField(u'时间线内容')
    submit = SubmitField(u'添加时间线')


@add_timeline_bp.route('/addTimeline')
def index():
    form = TimelineForm()
    if form.validate_on_submit():
        timeline_title = form.timeline_title
        timeline_content = form.timeline_content
    return render_template('/backend/addTimeline.html', form=form)

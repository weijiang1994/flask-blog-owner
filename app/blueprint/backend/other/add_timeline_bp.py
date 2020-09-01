"""
coding:utf-8
file: add_timeline_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/6/10 23:01
@desc:
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired
from ....model.blogin_model import Timeline
from ....model.db_operate import DBOperator
from ....util.common_util import get_uuid, get_current_time

add_timeline_bp = Blueprint('add_timeline_bp', __name__, url_prefix='/backend')


class TimelineForm(FlaskForm):
    timeline_title = StringField(u'名称', validators=[Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                                 render_kw={'class': '', 'rows': 50, 'placeholder': '请输入时间线标题'})
    timeline_content = TextAreaField(u'时间线内容', validators=[DataRequired()],
                                     render_kw={'placeholder': '请输入时间线内容，多条使用；隔开'})
    submit = SubmitField(u'添加时间线')


@add_timeline_bp.route('/addTimeline', methods=['GET', 'POST'])
def index():
    form = TimelineForm()
    if form.validate_on_submit():
        timeline_title = form.timeline_title.data
        timeline_content = form.timeline_content.data
        time_line = Timeline(id=get_uuid(), title=timeline_title, content=timeline_content, time=get_current_time())
        db = DBOperator()
        db.add_data(time_line)
        db.commit_data()
        return redirect(url_for('timeline_bp.index'))
    return render_template('/backend/addTimeline.html', form=form)

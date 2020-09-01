"""
coding:utf-8
file: timeline_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/4/14 22:33
@desc:
"""
from flask import Blueprint, render_template
from ..model.db_operate import DBOperator
from ..model.blogin_model import Timeline
from ..util.common_util import TIMELINE_STYLE
import random


timeline_bp = Blueprint('timeline_bp', __name__)


@timeline_bp.route('/timeline')
def index():
    ret = []
    db = DBOperator()
    time_lines = db.query_all(Timeline)
    for time_line in time_lines:
        ret.append([time_line.title, [content for content in time_line.content.split('；') if content != ''],
                    time_line.time, TIMELINE_STYLE[random.randint(0, 2)]])
    print(ret)
    return render_template('timeline.html', timelines=ret)


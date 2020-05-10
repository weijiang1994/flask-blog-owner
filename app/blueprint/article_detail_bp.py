"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
from flask import Blueprint, render_template, current_app
from ..model.db_operate import DBOperator
from ..model.blogin_model import Article
import traceback
article_detail_bp = Blueprint('article_detail_bp', __name__, url_prefix='/detail')


# 打开article类型文章详细页面
@article_detail_bp.route('/article/<title>', methods=['GET', 'POST'])
def index(title):
    try:
        current_app.config['current_article_title'] = title
        db = DBOperator()
        ret = db.query_filter_by_title(obj=Article, condition=title)[0]
        read_times = ret.read_times
        if ret.type == 1:
            article_type = '随记文章'
        else:
            article_type = '技术开发'
        ret.read_times += 1
        db.commit_data()
        return render_template('articleDetail.html', title=title, create_time='发布于' + str(ret.create_time),
                               read_times='阅读数' + str(read_times), article_type=article_type,
                               article_content=ret.content)
    except Exception as e:
        print(e.args)
        traceback.print_exc()
        return render_template('error/error.html')


@article_detail_bp.route('/content', methods=['GET', 'POST'])
def get_article_content():
    pass

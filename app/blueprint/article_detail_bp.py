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
@article_detail_bp.route('/article/<path:title>', methods=['GET', 'POST'])
def index(title):
    try:
        current_app.config['current_article_title'] = title
        db = DBOperator()
        ret = db.query_filter_by_title(obj=Article, condition=title)[0]
        articles = db.query_all_time(Article)

        current_index = 0
        pre_article = ''
        pre_link = ''
        next_article = ''
        next_link = ''

        for i, article in enumerate(articles):
            if article.title == title:
                current_index = i
                break
        if current_index == 0:
            pre_article = ''
            pre_link = ''
        else:
            pre_article = '<上一篇:'+articles[current_index-1].title
            pre_link = '/detail/article/'+articles[current_index-1].title
        if current_index == len(articles)-1:
            next_article = ''
            next_link = ''
        else:
            next_article = '下一篇:' + articles[current_index+1].title+'>'
            next_link = '/detail/article/'+articles[current_index+1].title
        read_times = ret.read_times

        # 文章阅读次数+1
        ret.read_times += 1
        db.commit_data()
        db.clear_buffer()
        del db
        return render_template('articleDetail.html', title=title, create_time='发布于' + str(ret.create_time),
                               read_times='阅读数' + str(read_times), article_type=ret.type,
                               article_content=ret.content, preLink=pre_link, preArticle=pre_article,
                               nextLink=next_link, nextArticle=next_article)
    except Exception as e:
        print(e.args)
        traceback.print_exc()
        return render_template('error/error.html')


@article_detail_bp.route('/content', methods=['GET', 'POST'])
def get_article_content():
    pass

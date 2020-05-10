"""
coding:utf-8
file: category_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/4/11 18:47
@desc:
"""
from flask import Blueprint, render_template, request
from ..model.blogin_model import Article, BlogType
from ..model.db_operate import DBOperator

category_dic = {'生活': 1, '陈词': 2, '技术': 3}
category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/category/', methods=['GET'])
def category():
    return render_template('category.html')


@category_bp.route('/category/<article>/', methods=['GET'])
def category_article(article):
    db = DBOperator()
    ret = db.query_filter_by_category_name(BlogType, condition=article)[0]
    ret2 = db.query_filter_by_category(Article, condition='1', page_index=1, page_size=10)
    print(ret2)
    db.clear_buffer()
    del db
    return render_template('category.html', category_name=article, category_article_count=ret.blog_count,
                           category_desc=ret.description)


@category_bp.route('/category/getBlogBrief', methods=['POST'])
def blog_brief():

    pass
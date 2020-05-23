"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
from flask import Blueprint, render_template, jsonify
from ..model.blogin_model import Article, BlogType
from ..model.db_operate import DBOperator
import math
index_bp = Blueprint('index_bp', __name__)
title_limit = 25
brief_limit = 90
page_size = 10


@index_bp.route('/')
def index():
    return render_template('home copy.html')


@index_bp.route('/blogBriefInfo/<int:page>', methods=['GET', 'POST'])
def get_blog_brief_info(page=None):
    ret = list()
    if page == 0:
        page = 1
    db = DBOperator()
    _data = db.query_all_desc_time(Article, page_size, page)
    total = db.query_all(Article)
    total = len(total)
    if total < page_size:
        total = 0
    else:
        total = math.ceil(total / page_size)
    for i in _data:
        sub = list()
        sub.append(str(i.create_time))
        if len(i.brief_content) > brief_limit:
            i.brief_content = i.brief_content[0:brief_limit] + '...'
        sub.append(i.title)
        sub.append(i.brief_content)
        sub.append(i.img)
        ret.append(sub)
    db.clear_buffer()

    db = DBOperator()
    blog_type_ls = list()
    blog_type_ret = db.query_all(BlogType)
    for i in blog_type_ret:
        sub = list()
        sub.append(i.type_name)
        sub.append(i.blog_count)
        blog_type_ls.append(sub)
    db.clear_buffer()
    del db
    return jsonify({'data': ret, 'total': total, 'blog_type': blog_type_ls})


@index_bp.route('/search')
def search_article():
    return

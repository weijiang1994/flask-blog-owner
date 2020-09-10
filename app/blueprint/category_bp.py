"""
coding:utf-8
file: category_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/4/11 18:47
@desc:
"""
import math

from flask import Blueprint, render_template, jsonify, g
from ..model.blogin_model import Article, BlogType, Notification
from ..model.db_operate import DBOperator

category_dic = {'生活': 1, '陈词': 2, '技术': 3}
category_bp = Blueprint('category_bp', __name__)
page_size = 10
brief_limit = 90


@category_bp.route('/category/', methods=['GET'])
def category():
    db = DBOperator()
    notifications = db.query_notification_by_receive_id(Notification, condition=g.normal_user)
    return render_template('category.html', ntf_counts=len(notifications))


@category_bp.route('/category/<article>/', methods=['GET'])
def category_article(article):
    db = DBOperator()
    ret = db.query_filter_by_category_name(BlogType, condition=article)[0]

    db.clear_buffer()
    del db
    return render_template('category.html', category_name=article, category_article_count=ret.blog_count,
                           category_desc=ret.description)


@category_bp.route('/category/getBlogBrief/<arc_type>/<page>', methods=['POST'])
def blog_brief(arc_type, page):
    ret_ls = list()
    arc_type = arc_type.split('：')[-1]
    if page == '0':
        page = 1
    page = int(page)
    db = DBOperator()
    ret = db.query_filter_by_category_name(BlogType, condition=arc_type)[0]
    total = ret.blog_count
    if total < page_size:
        total = 0
    else:
        total = math.ceil(total / page_size)

    ret2 = db.query_filter_by_category(Article, condition=arc_type, page_index=page,
                                       page_size=page_size)
    for i in ret2:
        sub = list()
        sub.append(str(i.create_time))
        if len(i.brief_content) > brief_limit:
            i.brief_content = i.brief_content[0:brief_limit] + '...'
        sub.append(i.title)
        sub.append(i.brief_content)
        sub.append(i.img)
        ret_ls.append(sub)
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
    return jsonify({'data': ret_ls, 'total': total, 'blog_type': blog_type_ls})

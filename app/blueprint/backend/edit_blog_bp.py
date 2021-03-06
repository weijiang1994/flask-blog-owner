"""
coding:utf-8
file: edit_blog_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/3/15 23:05
@desc:
"""
from flask import Blueprint, request, render_template, jsonify
from ...model.blogin_model import BlogType, Article
from ...model.db_operate import DBOperator
from ...util.common_util import get_uuid, get_current_time

edit_blog_bp = Blueprint('edit_blog_bp', __name__, url_prefix='/backend')

BLOG_STATE = {0: '正常', 1: '删除'}


@edit_blog_bp.route('/editBlog', methods=['GET', 'POST'])
def index():
    blog_type_datas = []
    articles_ret = []
    db_opr = DBOperator()
    blog_types = db_opr.query_all(obj=BlogType)
    articles = db_opr.query_all(obj=Article)
    for i, blog_type in enumerate(blog_types):
        blog_type_datas.append([blog_type.id, blog_type.type_name, blog_type.create_time, blog_type.blog_count,
                                blog_type.description, '/backend/editArticleType/' + blog_type.id])
    for i, article in enumerate(articles):
        articles_ret.append([article.id, article.title, article.type, article.brief_content[:30] + '...', article.create_time,
                             article.update_time, article.read_times, BLOG_STATE.get(article.delete_flag),
                             article.delete_flag])
    db_opr.clear_buffer()
    del db_opr
    return render_template('/backend/editBlog.html', blog_type_datas=blog_type_datas, articles=articles_ret)


@edit_blog_bp.route('/editArticleType/<type_id>', methods=['GET', 'POST'])
def edit_blog_type(type_id):
    db_opr = DBOperator()
    if request.method == 'POST':
        category_name = request.form.get('name')
        category_desc = request.form.get('desc')
        category = db_opr.update_blog_type_count(BlogType, condition=category_name)
        category[0].description = category_desc
        db_opr.commit_data()
        return jsonify({"tag": True})
    datas = db_opr.query_filter_by_id(obj=BlogType, condition=type_id)
    return render_template('backend/editBlogType.html', blog_type=datas[0].type_name, create_time=datas[0].create_time,
                           count=datas[0].blog_count, description=datas[0].description)


@edit_blog_bp.route('/addCategory', methods=['POST'])
def add_category():
    category_name = request.form.get('name')
    desc = request.form.get('desc')

    db_opr = DBOperator()
    categories = db_opr.query_filter_by_category_name(obj=BlogType, condition=category_name)
    if categories:
        return jsonify({"is_exists": True})
    type_obj = BlogType(id=get_uuid(), type_name=category_name, create_time=get_current_time(), blog_count=0,
                        description=desc)
    db_opr.add_data(type_obj)
    db_opr.commit_data()
    db_opr.clear_buffer()
    del db_opr
    return jsonify({"is_exists": False})


@edit_blog_bp.route('/deleteCategory', methods=['POST'])
def delete_category():
    category_id = request.form.get('id')
    db_opr = DBOperator()
    category = db_opr.query_filter_by_id(BlogType, condition=category_id)
    if category[0].blog_count:
        return jsonify({'not_null': True})
    db_opr.remove_data_by_id(BlogType, condition=category_id)
    db_opr.commit_data()
    return jsonify({'not_null': False})

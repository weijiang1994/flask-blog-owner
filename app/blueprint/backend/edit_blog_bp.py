"""
coding:utf-8
file: edit_blog_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/3/15 23:05
@desc:
"""
from flask import Blueprint, request, render_template
from ...model.blogin_model import BlogType
from ...model.db_operate import DBOperator

edit_blog_bp = Blueprint('edit_blog_bp', __name__, url_prefix='/backend')


@edit_blog_bp.route('/editBlog', methods=['GET', 'POST'])
def index():
    blog_type_datas = []
    db_opr = DBOperator()
    blog_types = db_opr.query_all(obj=BlogType)
    print(db_opr)
    for i, blog_type in enumerate(blog_types):
        print(i)
        print(blog_type.id)
        blog_type_datas.append([blog_type.id, blog_type.type_name, blog_type.create_time, blog_type.blog_count,
                               blog_type.description, '/backend/editArticleType/'+blog_type.id])
    return render_template('/backend/editBlog.html', blog_type_datas=blog_type_datas)


@edit_blog_bp.route('/editArticleType/<int:type_id>')
def edit_blog_type(type_id):
    print(type_id)
    db_opr = DBOperator()
    datas = db_opr.query_filter_by_id(obj=BlogType, condition=type_id)
    return render_template('backend/editBlogType.html', blog_type=datas[0].type_name, create_time=datas[0].create_time,
                           count=datas[0].blog_count, description=datas[0].description)

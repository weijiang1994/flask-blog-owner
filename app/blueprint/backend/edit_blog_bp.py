"""
coding:utf-8
file: edit_blog_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/3/15 23:05
@desc:
"""
from flask import Blueprint, request, render_template

edit_blog_bp = Blueprint('edit_blog_bp', __name__, url_prefix='/backend')


@edit_blog_bp.route('/editBlog', methods=['GET', 'POST'])
def index():
    return render_template('/backend/editBlog.html')

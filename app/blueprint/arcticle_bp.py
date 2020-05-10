"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
from flask import Blueprint, render_template

article_bp = Blueprint('article_bp',  __name__)


@article_bp.route('/article')
def article():
    return render_template('article.html')

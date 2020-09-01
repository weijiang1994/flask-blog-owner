"""
# coding:utf-8
@Time    : 2020/9/1
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : search_blog
@Software: PyCharm
"""
from flask import Blueprint, request, render_template
from ..model.db_operate import DBOperator
from ..model.blogin_model import Article

search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/search/', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'GET':
        keyword = request.args.get('q')
        db = DBOperator()
        blogs = db.contain_query(Article, keyword)
        for blog in blogs:
            results.append({'title': blog.title, 'brief_content': blog.brief_content})
    else:
        keyword = request.form.get('q')
    return render_template('searchResult.html', blogs=results)

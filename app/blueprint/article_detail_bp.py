"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
from flask import Blueprint, render_template, current_app, request, redirect, g
from urllib import parse
from ..model.db_operate import DBOperator
from ..model.blogin_model import Article, Users
import traceback
from ..model.db_operate import DBOperator
from ..model.blogin_model import Comment
from ..util.common_util import get_current_time

article_detail_bp = Blueprint('article_detail_bp', __name__, url_prefix='/detail')


# 打开article类型文章详细页面
@article_detail_bp.route('/article/<path:title>/', methods=['GET', 'POST'])
def index(title):
    try:
        current_app.config['current_article_title'] = title
        comments_ret = []
        db = DBOperator()
        ret = db.query_filter_by_title(obj=Article, condition=title)[0]
        articles = db.query_all_time(Article)

        current_index = 0
        # pre_article = ''
        # pre_link = ''
        # next_article = ''
        # next_link = ''
        # comment_count = 0
        for i, article in enumerate(articles):
            if article.title == title:
                current_index = i
                break
        if current_index == 0:
            pre_article = ''
            pre_link = ''
        else:
            pre_article = '<上一篇:' + articles[current_index - 1].title
            pre_link = '/detail/article/' + articles[current_index - 1].title
        if current_index == len(articles) - 1:
            next_article = ''
            next_link = ''
        else:
            next_article = '下一篇:' + articles[current_index + 1].title + '>'
            next_link = '/detail/article/' + articles[current_index + 1].title
        read_times = ret.read_times

        # 文章阅读次数+1
        ret.read_times += 1
        db.commit_data()

        # 获取该篇文章总评论数
        comments = db.query_comment_by_blog_id(Comment, condition=ret.id)
        comment_count = len(comments)
        # 获取该篇文章的顶级评论
        comments = db.query_top_comment_by_blog_id(Comment, condition=ret.id)
        for comment in comments:
            comm = []
            user = db.query_filter_by_id(Users, comment.create_u_id)
            top_comment = [user[0].avatar, user[0].username, comment.comment_content, comment.comment_time, comment.id]
            comm.append(top_comment)
            # 查询该顶级评论的子评论按照时间升序
            children = db.query_child_comment(Comment, comment.id)
            if len(children) == 0:
                comm.append([])
            else:
                pass
            comments_ret.append(comm)
        db.clear_buffer()
        del db
        return render_template('articleDetail.html', title=title, create_time='发布于' + str(ret.create_time),
                               read_times='阅读数' + str(read_times), article_type=ret.type,
                               article_content=ret.content, preLink=pre_link, preArticle=pre_article,
                               nextLink=next_link, nextArticle=next_article, comment_count=comment_count,
                               comments=comments_ret)
    except Exception as e:
        print(e.args)
        traceback.print_exc()
        return render_template('error/error.html')


@article_detail_bp.route('/comment/', methods=['GET', 'POST'])
def submit_comment():
    comment = request.form.get('comment-editor')
    blog_title = parse.unquote(request.referrer.split('/')[-2])
    db = DBOperator()
    blog = db.query_filter_by_title(Article, condition=blog_title)[0]
    comm = Comment(create_u_id=g.normal_user, article_id=blog.id, parent_id=None, comment_time=get_current_time(),
                   comment_content=comment, delete_flag=0)
    db.add_data(comm)
    db.commit_data()
    db.clear_buffer()
    del db
    return redirect(request.referrer)


@article_detail_bp.route('/replyComment/', methods=['GET', 'POST'])
def reply_comment():
    reply_comment = request.form.get('reply_comment')
    # 1. 保存用户回复的评论
    # 2. 添加notification
    db = DBOperator()
    comment = Comment()
    db.add_data()
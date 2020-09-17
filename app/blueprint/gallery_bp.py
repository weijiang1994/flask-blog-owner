"""
coding:utf-8
file: gallery_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/06/02 23:00
@desc:
"""
import functools
from flask import Blueprint, render_template, request, jsonify, g, redirect
from app.decorators import confirm_required
from .login_bp import user_login_require
from ..model.db_operate import DBOperator
from ..model.blogin_model import Gallery, Tags, PhotoTag, Notification, Likes, LikePhoto, Comment, PhotoComment, Users
from ..util.common_util import get_current_time

gallery_bp = Blueprint('gallery_bp', __name__)


def ajax_redirect_login(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.normal_user is None:
            return jsonify({'url': '/auth/userLogin'})
        print(view is None)
        return view(**kwargs)
    return wrapped_view


@gallery_bp.route('/gallery')
def gallery():
    ret = []
    db = DBOperator()
    galleries = db.query_all(Gallery)
    notifications = db.query_notification_by_receive_id(Notification, condition=g.normal_user)
    for photo in galleries:
        likes = db.query_like_by_photo_id(Likes, photo.id)
        if likes:
            like_counts = likes.like_counts
        else:
            like_counts = 0
        ret.append([photo.photo_title, photo.photo_path, photo.create_time, photo.id,
                    like_counts])

    return render_template('gallery.html', galleries=ret, ntf_counts=len(notifications))


@gallery_bp.route('/getPhoto', methods=['POST'])
def get_photo():
    if request.method == 'POST':
        db = DBOperator()
        ret = db.query_all(Gallery)
        total_photo = len(ret)
        photo_info = list()
        for i in ret:
            sub = list()
            sub.append(i.photo_title)
            sub.append(i.photo_path)
            sub.append(i.photo_desc)
            photo_info.append(sub)
        return jsonify({'photo_info': photo_info, 'total': total_photo})


@gallery_bp.route('/photo/<photo_id>', methods=['GET', 'POST'])
def show_photo(photo_id):
    db = DBOperator()
    tags_ls = []
    tags_id = []
    photo = db.query_filter_by_id(Gallery, condition=photo_id)[0]
    photos = db.query_all(Gallery)
    tags = db.query_photo_tag_by_id(Tags, condition=photo.id)
    notifications = db.query_notification_by_receive_id(Notification, condition=g.normal_user)
    if len(tags) != 0:
        for tag in tags:
            photo_tag = db.query_filter_by_id(PhotoTag, condition=tag.tag_id)[0]
            tags_ls.append(photo_tag.tag_name)
            tags_id.append(photo_tag.id)

    current_idx = 0
    # 获取上一个下一个照片
    for i, ph in enumerate(photos):
        if photo.id == ph.id:
            current_idx = i
    if current_idx == 0:
        pre_link = ''
    else:
        pre_link = '/photo/' + photos[current_idx - 1].id
    if current_idx == len(photos) - 1:
        next_link = ''
    else:
        next_link = '/photo/' + photos[current_idx + 1].id
    if g.normal_user:
        user_id = g.normal_user
        judge_like = db.query_by_like_user_id(LikePhoto, user_id, photo_id)
        if judge_like:
            like = 'unlike'
            pre_like = '取消'
        else:
            like = 'like'
            pre_like = '给'
    else:
        like = ''
        pre_like = '给'
    # 获取当前照片评论数
    comments_ret = []
    comment_count, deleted_counts = get_photo_comment(comments_ret, db, photo_id)
    # 拼接数据返回渲染
    ret = {'title': photo.photo_title, 'photo': photo.photo_path, 'photoDesc': photo.photo_desc,
           'updateTime': photo.create_time, 'preLink': pre_link, 'nextLink': next_link, 'tags': tags_ls,
           'tagIds': tags_id, 'like': like, 'pre_like': pre_like}

    return render_template('showPhoto.html', photo=ret, photoDesc=photo.photo_desc,
                           time=photo.create_time, ntf_counts=len(notifications), comment_count=comment_count,
                           comment_ret=comments_ret, deleted=deleted_counts)


def get_photo_comment(comments_ret, db, photo_id):
    comments = db.query_top_pc_by_blog_id(PhotoComment, condition=photo_id)
    comment_count = len(comments)
    deleted_count = 0
    for comment in comments:
        # 统计当前照片被删除的评论条数
        if '该条评论已删除' in comment.content:
            deleted_count += 1
        comm = []
        child_comm = []
        user = db.query_filter_by_id(Users, comment.user_id)
        top_comment = [user[0].avatar, user[0].username, comment.content, comment.comm_timestamp, comment.id]
        comm.append(top_comment)
        children = db.query_child_comment(PhotoComment, comment.id)
        if len(children) == 0:
            comm.append([])
        else:
            for child in children:
                usr = db.query_filter_by_id(Users, condition=child.user_id)[0]
                avatar = usr.avatar
                username = usr.username
                child_comment = child.content
                child_comm_time = child.comm_timestamp
                parent_id = comment.id
                child_id = child.id
                child_comm.append([avatar, username, child_comment, child_comm_time, parent_id, child_id])
            comm.append(child_comm)
        comments_ret.append(comm)
    return comment_count, deleted_count


@gallery_bp.route('/gallery/tag/<int:tag_id>', methods=['GET', 'POST'])
def get_photo_tag(tag_id):
    db = DBOperator()
    tags = db.query_photo_by_tag_id(Tags, condition=tag_id)
    tag_name = db.query_filter_by_id(PhotoTag, condition=tag_id)[0].tag_name
    photo_ids = []
    photos = []
    for tag in tags:
        photo_ids.append(tag.photo_id)
    for ph_id in photo_ids:
        photo = db.query_filter_by_id(Gallery, condition=ph_id)[0]
        photos.append([photo.photo_title, photo.photo_path, photo.create_time, photo.id])
    return render_template('photoTag.html', galleries=photos, tag=tag_name)


@gallery_bp.route('/gallery/comment/', methods=['POST'])
@user_login_require
@confirm_required
def photo_comment():
    ph_id = request.referrer.split('/')[-1]
    usr_id = g.normal_user
    comm_content = request.form.get('comment-editor')
    db = DBOperator()
    pc = PhotoComment(photo_id=ph_id, user_id=usr_id, comm_timestamp=get_current_time(), content=comm_content,
                      parent_id=None)
    db.add_data(pc)
    db.commit_data()
    return redirect(request.referrer)


# noinspection PyBroadException
@gallery_bp.route('/gallery/like/', methods=['POST'])
@ajax_redirect_login
@confirm_required
def like_photo():
    try:
        # 获取当前照片的id
        photo_id = request.referrer.split('/')[-1]

        db = DBOperator()
        like = db.query_filter_by_photo_id(Likes, condition=photo_id)
        if like:
            like.like_counts += 1
        else:
            new_like = Likes(photo_id=photo_id, like_counts=1)
            db.add_data(new_like)
        lk_ph = LikePhoto(photo_id=photo_id, like_user_id=g.normal_user, like_time=get_current_time(), delete_flag=0)
        db.add_data(lk_ph)
        db.commit_data()
        return jsonify({'tag': 1, 'info': '点赞成功啦~开心ing ☺'})

    except:
        import traceback
        traceback.print_exc()
        return jsonify({'tag': 0, 'info': '点赞失败~'})


# noinspection PyBroadException
@gallery_bp.route('/gallery/unlike/', methods=['POST'])
@ajax_redirect_login
@confirm_required
def photo_unlike():
    try:
        ph_id = request.referrer.split('/')[-1]
        usr_id = g.normal_user
        db = DBOperator()
        db.delete_like(LikePhoto, condition=ph_id, condition2=usr_id)
        db.query_like_by_photo_id(Likes, ph_id).like_counts -= 1
        db.commit_data()
        return jsonify({'tag': 1, 'info': '取消点赞成功～不开心ing'})
    except:
        return jsonify({'tag': 0, 'info': '取消点赞失败~'})


@gallery_bp.route('/gallery/comment/delete/', methods=['POST'])
@ajax_redirect_login
def delete_photo_comment():
    try:
        comm_id = request.form.get('comm_id')
        db = DBOperator()
        target_comment = db.query_filter_by_id(PhotoComment, condition=comm_id)[0]
        target_comment.content = '该条评论已删除'
        db.commit_data()
        return jsonify({'tag': 1, 'info': '评论删除成功'})
    except:
        import traceback
        traceback.print_exc()
        return jsonify({'tag': 1, 'info': '评论删除失败'})


@gallery_bp.route('/gallery/comment/reply/', methods=['POST'])
@ajax_redirect_login
def reply_photo_comment():
    rep_content = request.form.get('reply_comment')
    receive_u = request.form.get('receive_u')
    parent_id = request.form.get('parent_id')
    ph_id = request.referrer.split('/')[-1]
    db = DBOperator()
    pc = PhotoComment(content=rep_content, parent_id=parent_id, user_id=g.normal_user,
                      comm_timestamp=get_current_time(), photo_id=ph_id)
    db.add_data(pc)
    db.commit_data()
    return jsonify({'tag': 1, 'info': '评论成功'})

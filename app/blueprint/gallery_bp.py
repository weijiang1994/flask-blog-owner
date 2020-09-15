"""
coding:utf-8
file: gallery_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/06/02 23:00
@desc:
"""
from flask import Blueprint, render_template, request, jsonify, g

from .login_bp import user_login_require
from ..model.db_operate import DBOperator
from ..model.blogin_model import Gallery, Tags, PhotoTag, Notification, Likes, LikePhoto
from ..util.common_util import get_current_time

gallery_bp = Blueprint('gallery_bp', __name__)


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
    # 拼接数据返回渲染
    ret = {'title': photo.photo_title, 'photo': photo.photo_path, 'photoDesc': photo.photo_desc,
           'updateTime': photo.create_time, 'preLink': pre_link, 'nextLink': next_link, 'tags': tags_ls,
           'tagIds': tags_id, 'like': like, 'pre_like': pre_like}
    return render_template('showPhoto.html', photo=ret, photoDesc=photo.photo_desc,
                           time=photo.create_time, ntf_counts=len(notifications))


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


@gallery_bp.route('/gallery/like/', methods=['POST'])
@user_login_require
def like_photo():
    # noinspection PyBroadException
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


@gallery_bp.route('/gallery/unlike/', methods=['POST'])
@user_login_require
def photo_unlike():
    # noinspection PyBroadException
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

"""
coding:utf-8
file: gallery_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/06/02 23:00
@desc:
"""
from flask import Blueprint, render_template, request, jsonify, g
from ..model.db_operate import DBOperator
from ..model.blogin_model import Gallery, Tags, PhotoTag, Notification

gallery_bp = Blueprint('gallery_bp', __name__)


@gallery_bp.route('/gallery')
def gallery():
    ret = []
    db = DBOperator()
    galleries = db.query_all(Gallery)
    notifications = db.query_notification_by_receive_id(Notification, condition=g.normal_user)
    for photo in galleries:
        ret.append([photo.photo_title, photo.photo_path, photo.create_time, photo.id])
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

    # 拼接数据返回渲染
    ret = {'title': photo.photo_title, 'photo': photo.photo_path, 'photoDesc': photo.photo_desc,
           'updateTime': photo.create_time, 'preLink': pre_link, 'nextLink': next_link, 'tags': tags_ls,
           'tagIds': tags_id}
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

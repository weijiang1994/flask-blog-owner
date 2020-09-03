"""
coding:utf-8
file: gallery_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/06/02 23:00
@desc:
"""
from flask import Blueprint, render_template, request, jsonify, redirect
from ..model.db_operate import DBOperator
from ..model.blogin_model import Gallery

gallery_bp = Blueprint('gallery_bp', __name__)


@gallery_bp.route('/gallery')
def gallery():
    ret = []
    db = DBOperator()
    galleries = db.query_all(Gallery)
    for photo in galleries:
        ret.append([photo.photo_title, photo.photo_path, photo.create_time, photo.id])
    return render_template('gallery.html', galleries=ret)


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
    photo = db.query_filter_by_id(Gallery, condition=photo_id)[0]
    photos = db.query_all(Gallery)
    current_idx = 0
    for i, ph in enumerate(photos):
        if photo.id == ph.id:
            current_idx = i
    if current_idx == 0:
        pre_link = ''
    else:
        pre_link = '/photo/'+photos[current_idx-1].id
    if current_idx == len(photos) - 1:
        next_link = ''
    else:
        next_link = '/photo/'+photos[current_idx+1].id
    print('pre link:', pre_link)
    print('next link', next_link)

    ret = {'title': photo.photo_title, 'photo': photo.photo_path, 'photoDesc': photo.photo_desc,
           'updateTime': photo.create_time, 'preLink': pre_link, 'nextLink': next_link
           }
    print(ret)
    return render_template('showPhoto.html', photo=ret, photoDesc=photo.photo_desc,
                           time=photo.create_time, )


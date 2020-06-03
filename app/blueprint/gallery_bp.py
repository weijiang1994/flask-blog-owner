"""
coding:utf-8
file: gallery_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/06/02 23:00
@desc:
"""
from flask import Blueprint, render_template, request, jsonify
from ..model.db_operate import DBOperator
from ..model.blogin_model import Gallery

gallery_bp = Blueprint('gallery_bp', __name__)


@gallery_bp.route('/article')
def article():
    return render_template('/gallery/index.html')


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

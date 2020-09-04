"""
# coding:utf-8
@Time    : 2020/9/3
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : edit_photo_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template

edit_photo_bp = Blueprint('edit_photo_bp', __name__, url_prefix='/backend')


@edit_photo_bp.route('editPhoto')
def index():
    return render_template('backend/editPhoto.html')

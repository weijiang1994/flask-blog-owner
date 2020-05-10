"""
coding:utf-8
file: admin_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/3/14 21:31
@desc:
"""
from flask import Blueprint, request, render_template
from .login_bp import login_require
admin_bp = Blueprint('admin_bp', __name__, url_prefix='/backend')


@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_require
def index():
    if request.method == 'POST':
        pass
    return render_template('/backend/admin.html')

"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
import json

from flask import Blueprint, render_template, request, jsonify

own_bp = Blueprint('own_bp',  __name__)


@own_bp.route('/aboutMe')
def article():
    return render_template('own.html')


@own_bp.route('/authority', methods=['POST'])
def authority_pwd():
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        if data['pwd'] == 'jiangW3521946.':
            return jsonify({'tag': 0, 'src': '../static/img/resume.jpg'})
    return jsonify({'tag': 1})

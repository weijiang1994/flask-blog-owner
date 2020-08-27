"""
coding:utf-8
file: login_bp.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/1/14 23:00
@desc:
"""
from flask import Blueprint, render_template, request, jsonify
from ..util.common_util import get_encrypt_text

work_bp = Blueprint('work_bp',  __name__)


@work_bp.route('/tech')
def article():
    return render_template('tool.html')


@work_bp.route('/tech/encrypt', methods=['POST'])
def generate_encrypt_text():
    text = request.form.get('text')
    encrypt_way = request.form.get('encryptWay')
    output_way = request.form.get('outputWay')
    encrypt_text = get_encrypt_text(encrypt_way, text)
    if output_way == '大写':
        encrypt_text = encrypt_text.upper()
    return jsonify({'encryptText': encrypt_text})

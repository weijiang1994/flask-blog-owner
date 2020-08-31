"""
# coding:utf-8
@Time    : 2020/8/31
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : wsgi
@Software: PyCharm
"""
from app import create_app

app = create_app('production')

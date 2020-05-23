"""
@Time    : 2020/1/3 14:21
@Author  : weijiang
@Site    : 
@File    : common_util.py
@Software: PyCharm
@License: (@)Copyright 2001-2019,SZ_Colibri
@Contact:weijiang@colibri.com.cn
"""
import os
import uuid
import datetime
import hashlib

CATEGORY_DIC = {1: '生活', 2: '陈词', 3: '技术'}


def get_uuid():
    """
    get the uuid text
    :return: uuid text
    """
    return str(uuid.uuid1()).replace('-', '')


def get_current_time():
    """
    get the current time with yy-mm-dd hh:mm:ss format
    :return: the current time
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_md5(plaintext):
    """
    get the encrypted text with md5 algorithm
    :param plaintext: need to encryption plaintext
    :return: ciphertext
    """
    _md5 = hashlib.md5()
    b = plaintext.encode(encoding='utf-8')
    _md5.update(b)
    return _md5.hexdigest()


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

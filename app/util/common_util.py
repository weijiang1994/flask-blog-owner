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
import configparser

from dateutil.parser import parse
from flask import current_app
from ..frozen_dir import app_path
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
import base64

AVATARS = ['/static/avatars/1.jpg', '/static/avatars/2.jpg', '/static/avatars/3.jpg', '/static/avatars/4.jpg',
           '/static/avatars/5.png', '/static/avatars/6.png', '/static/avatars/7.png', '/static/avatars/8.png',
           '/static/avatars/9.png', '/static/avatars/10.png']

CATEGORY_DIC = {1: '生活', 2: '陈词', 3: '技术'}
SUPER_DIR = app_path()
CONFIG_PATH = app_path() + r'/config/config.ini'

TIMELINE_STYLE = [['cd-location', 'cd-icon-location.svg'], ['cd-movie', 'cd-icon-movie.svg'],
                  ['cd-picture', 'cd-icon-picture.svg'], ]


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class ReadConfig:

    def __init__(self, config_path=None):
        self.cf = configparser.ConfigParser()
        self.cf.read(config_path)

    def get_database(self, param):
        return self.cf.get('DATABASE', param)


DB_HOST = ReadConfig(CONFIG_PATH).get_database('host')
DB_PORT = ReadConfig(CONFIG_PATH).get_database('port')
DB_USER = ReadConfig(CONFIG_PATH).get_database('user')
DB_PASSWORD = ReadConfig(CONFIG_PATH).get_database('password')
DB_DATABASE = ReadConfig(CONFIG_PATH).get_database('database')


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


def get_base64(text: str):
    return base64.encodebytes(text.encode('utf-8'))


def get_encrypt_text(way, text):
    if way == 'md5':
        return get_md5(text)
    if way == 'base64':
        return get_base64(text).decode('utf-8')


def get_time_delta(target_time):
    cu_time = get_current_time()
    cu_time = parse(str(cu_time))
    target_time = parse(str(target_time))
    total_sec = int((cu_time - target_time).total_seconds())
    if total_sec <= 30:
        return '刚刚'
    # 没超过分钟
    elif 30 < total_sec <= 60:
        return str(total_sec) + '秒之前'
    # 超过一分钟
    elif 60 < total_sec < 3600:
        minutes = total_sec // 60
        secs = total_sec % 60
        if secs == 0:
            return str(minutes) + '分之前'
        else:
            return str(minutes) + '分' + str(secs) + '秒之前'
    # 超过一小时
    elif 3600 <= total_sec < 60 * 60 * 24:
        hours = total_sec // 3600
        minutes = total_sec % 3600 // 60
        secs = total_sec % 3600 % 60
        if minutes == 0 and secs != 0:
            return str(hours) + '小时' + str(secs) + '秒之前'
        elif minutes != 0 and secs == 0:
            return str(hours) + '小时' + str(minutes) + '分之前'
        elif minutes == 0 and secs == 0:
            return str(hours) + '小时之前'
        else:
            return str(hours) + '小时' + str(minutes) + '分' + str(secs) + '秒之前'
    # 超过一天
    elif 60 * 60 * 24 <= total_sec < 60 * 60 * 24 * 365:
        days = total_sec // (60 * 60 * 24)
        return str(days) + '天之前'
    else:
        years = total_sec // (60 * 60 * 24 * 365)
        return str(years) + '年之前'


# 生成token
def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        user.confirmed = 1
    else:
        user.password = get_md5(new_password)

    return True


def generate_ver_code():
    import random
    return random.randint(134299, 873242)

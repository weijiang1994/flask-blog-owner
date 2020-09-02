"""
# coding:utf-8
@Time    : 2020/8/24
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : init_db
@Software: PyCharm
"""
import sys

import pymysql
import traceback

print('Starting the create database operation, please enter the information required for the database.')
print('-'*56)
host = input('please input database host:')
port = input('please input database port:')
user = input('please input database user:')
password = input('please input database password:')
print('-'*56)
try:
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='weijiang', password='1994124')
    conn = pymysql.connect(host=host, port=int(port), user=user, password=password)
    cursor = conn.cursor()
except Exception as e:
    print(e.args)
    traceback.print_exc()
    sys.exit()
try:
    # 创建数据库
    print('starting create database.')
    CREATE_DB_SQL = 'CREATE DATABASE IF NOT EXISTS blogin_test CHARACTER SET utf8 COLLATE utf8_general_ci'
    cursor.execute(CREATE_DB_SQL)
    conn.select_db('blogin_test')
    print('Created database is done.')
    print('-'*56)
    print('staring create gallery table.')
    CREATE_GALLERY_TABLE_SQL = "CREATE TABLE IF NOT EXISTS gallery (" \
                               "id VARCHAR (40) PRIMARY KEY NOT NULL ," \
                               "photo_title VARCHAR (255) NOT NULL ," \
                               "photo_path VARCHAR (255) NOT NULL ," \
                               "photo_desc VARCHAR (512) NOT NULL ," \
                               "create_time datetime NOT NULL ," \
                               "delete_flag INTEGER NOT NULL ," \
                               "private_flag INTEGER NOT NULL )"
    cursor.execute(CREATE_GALLERY_TABLE_SQL)
    print('the gallery table is created.')
    print('-'*56)
    print('starting create admin table.')
    CREATE_ADMIN_TABLE_SQL = "CREATE TABLE IF NOT EXISTS admin(" \
                             "id VARCHAR (40) PRIMARY KEY NOT NULL ," \
                             "user_name VARCHAR (255) NOT NULL ," \
                             "password VARCHAR (255) NOT NULL )"
    cursor.execute(CREATE_ADMIN_TABLE_SQL)
    print('the admin table is created.')
    print('-'*56)
    print('starting create timeline table.')
    CREATE_TIMELINE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS timeline(" \
                                "id VARCHAR (40) PRIMARY KEY  NOT NULL ," \
                                "title VARCHAR (255) NOT NULL ," \
                                "content VARCHAR (1024) NOT NULL ," \
                                "time datetime NOT NULL )"
    cursor.execute(CREATE_TIMELINE_TABLE_SQL)
    print('the timeline table is created.')
    print('-'*56)
    print('starting create blogtype table.')
    CREATE_BLOGTYPE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS blog_type(" \
                                "id VARCHAR (40) PRIMARY KEY NOT NULL ," \
                                "type_name VARCHAR (40) NOT NULL DEFAULT ''," \
                                "create_time datetime NOT NULL ," \
                                "blog_count INTEGER NOT NULL DEFAULT 0 ," \
                                "description VARCHAR (1024) NOT NULL DEFAULT '')"
    cursor.execute(CREATE_BLOGTYPE_TABLE_SQL)
    print('the blogtype table is created.')
    print('-'*56)
    print('starting create article table.')
    CREATE_ARTICLE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS article(" \
                               "id VARCHAR (40) PRIMARY KEY NOT NULL," \
                               "title VARCHAR (235) NOT NULL DEFAULT ''," \
                               "type VARCHAR(255) NOT NULL DEFAULT ''," \
                               "img VARCHAR (255) NOT NULL DEFAULT ''," \
                               "brief_content VARCHAR (255) NOT NULL DEFAULT ''," \
                               "content TEXT NOT NULL ," \
                               "is_private INTEGER NOT NULL DEFAULT 0," \
                               "create_time datetime NOT NULL ," \
                               "update_time datetime NOT NULL ," \
                               "read_times INTEGER NOT NULL DEFAULT 0," \
                               "delete_flag INTEGER NOT NULL DEFAULT 0)"
    cursor.execute(CREATE_ARTICLE_TABLE_SQL)
    print('the article table is created.')
    print('-'*56)
    print('starting create comment table')
    CREATE_COMMENT_TABLE_SQL = "CREATE TABLE IF NOT EXISTS comment(" \
                               "id VARCHAR (40) PRIMARY KEY NOT NULL ," \
                               "article_id VARCHAR (40) NOT NULL ," \
                               "parent_id VARCHAR (40) NOT NULL ," \
                               "comment_time datetime NOT NULL ," \
                               "comment_content VARCHAR (255) NOT NULL DEFAULT ''," \
                               "is_read INTEGER NOT NULL DEFAULT 0," \
                               "delete_flag INTEGER NOT NULL DEFAULT 0)"
    cursor.execute(CREATE_COMMENT_TABLE_SQL)
    print('the comment table is created.')
    print('-'*56)
    print('starting create like_blog table')
    CREATE_LIKEBLOG_TABLE_SQL = "CREATE TABLE IF NOT EXISTS like_blog(" \
                                "id VARCHAR (255) PRIMARY KEY NOT NULL DEFAULT ''," \
                                "blog_id VARCHAR (255) NOT NULL DEFAULT ''," \
                                "like_acount VARCHAR (255) NOT NULL DEFAULT ''," \
                                "like_time VARCHAR (255) NOT NULL DEFAULT '')"
    print('the like_blog table is created.')
    print('-'*56)
    conn.commit()
    print('database is initialed.')
except Exception as e:
    print(e.args)
    traceback.print_exc()

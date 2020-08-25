"""
@Time    : 2020/1/3 13:31
@Author  : weijiang
@Site    : 
@File    : db_operate.py
@Software: PyCharm
@License: (@)Copyright 2001-2019,SZ_Colibri
@Contact:weijiang@colibri.com.cn
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBOperator:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://weijiang:1994124@127.0.0.1:3306/blogin?charset=utf8')
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

    def add_data(self, obj):
        self.session.add(obj)

    def commit_data(self):
        self.session.commit()

    def query_all(self, obj):
        return self.session.query(obj).all()

    def query_all_time(self, obj):
        return self.session.query(obj).order_by(obj.create_time.desc()).all()

    def query_pre_article(self, obj, condition):
        return self.session.query(obj).filter_by(title=condition).order_by('create_time').first()

    def query_all_desc_time(self, obj, page_size, page_index):
        return self.session.query(obj).order_by(obj.create_time.desc()).\
            limit(page_size).offset((page_index-1)*page_size)

    def query_filter_by_id(self, obj, condition):
        ret = self.session.query(obj).filter_by(id=condition).all()
        return ret

    def query_filter_by_title(self, obj, condition):
        ret = self.session.query(obj).filter_by(title=condition).all()
        return ret

    def query_filter_by_category(self, obj, condition, page_size, page_index):
        ret = self.session.query(obj).filter_by(type=condition).order_by(obj.create_time.desc()).\
            limit(page_size).offset((page_index-1)*page_size)
        return ret

    def query_filter_by_category_name(self, obj, condition):
        ret = self.session.query(obj).filter_by(type_name=condition).all()
        return ret

    def update_blog_type_count(self, obj, condition):
        ret = self.session.query(obj).filter_by(type_name=condition).all()
        return ret

    def remove_data_by_id(self, obj, condition):
        ret = self.session.query(obj).filter_by(id=condition).first()
        self.session.delete(ret)

    def roll_back(self):
        self.session.roolback()

    def clear_buffer(self):
        self.engine.dispose()

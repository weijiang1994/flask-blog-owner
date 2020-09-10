"""
@Time    : 2020/1/3 13:31
@Author  : weijiang
@Site    : 
@File    : db_operate.py
@Software: PyCharm
@License: (@)Copyright 2001-2019,SZ_Colibri
@Contact:weijiang@colibri.com.cn
"""
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from ..util.common_util import DB_HOST, DB_PORT, DB_USER, DB_DATABASE, DB_PASSWORD

_engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.
                        format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE))
_session = sessionmaker(bind=_engine)
_session = scoped_session(_session)


class DBOperator:
    def __init__(self, engine=_engine, session=_session):
        self.engine = engine
        self.session = session

    def add_data(self, obj):
        self.session.add(obj)

    def commit_data(self):
        self.session.commit()

    def query_all(self, obj):
        return self.session.query(obj).all()

    def query_all_by_id(self, obj):
        return self.session.query(obj).order_by(obj.id.desc()).all()

    def query_all_time(self, obj):
        return self.session.query(obj).order_by(obj.create_time.desc()).all()

    def query_pre_article(self, obj, condition):
        return self.session.query(obj).filter_by(title=condition).order_by('create_time').first()

    def query_user_by_email(self, obj, condition):
        return self.session.query(obj).filter_by(email=condition).first()

    def query_user_by_name(self, obj, condition):
        return self.session.query(obj).filter_by(username=condition).first()

    def query_by_user_id(self, obj, condition):
        return self.session.query(obj).filter_by(user_id=condition).order_by(obj.login_time.desc()).first()

    def query_all_desc_time(self, obj, page_size, page_index):
        return self.session.query(obj).order_by(obj.create_time.desc()). \
            limit(page_size).offset((page_index - 1) * page_size)

    def query_comment_by_blog_id(self, obj, condition):
        return self.session.query(obj).filter_by(article_id=condition).order_by(obj.comment_time.desc()).all()

    def query_top_comment_by_blog_id(self, obj, condition):
        return self.session.query(obj).filter_by(article_id=condition, parent_id=None).order_by(obj.comment_time.
                                                                                                desc()).all()

    def query_filter_by_id(self, obj, condition):
        ret = self.session.query(obj).filter_by(id=condition).all()
        return ret

    def query_notification_by_receive_id(self, obj, condition):
        return self.session.query(obj).filter_by(receive_u=condition, readed=0).all()

    def query_child_comment(self, obj, condition):
        return self.session.query(obj).filter_by(parent_id=condition).all()

    def query_photo_tag_by_id(self, obj, condition):
        ret = self.session.query(obj).filter_by(photo_id=condition).all()
        return ret

    def query_filter_by_title(self, obj, condition):
        ret = self.session.query(obj).filter_by(title=condition).all()
        return ret

    def query_filter_by_category(self, obj, condition, page_size, page_index):
        ret = self.session.query(obj).filter_by(type=condition).order_by(obj.create_time.desc()). \
            limit(page_size).offset((page_index - 1) * page_size)
        return ret

    def query_filter_by_category_name(self, obj, condition):
        ret = self.session.query(obj).filter_by(type_name=condition).all()
        return ret

    def contain_query(self, obj, condition):
        ret = self.session.query(obj).filter(or_(obj.title.like('%{}%'.format(condition)),
                                                 obj.brief_content.like('%{}%'.format(condition)),
                                                 obj.content.like('%{}%'.format(condition))))
        return ret

    def query_tag_by_tag_name(self, obj, condition):
        ret = self.session.query(obj).filter_by(tag_name=condition).all()
        return ret

    def query_photo_by_tag_id(self, obj, condition):
        ret = self.session.query(obj).filter_by(tag_id=condition).all()
        return ret

    def update_blog_type_count(self, obj, condition):
        ret = self.session.query(obj).filter_by(type_name=condition).all()
        return ret

    def update_photo_count(self, obj, condition):
        ret = self.session.query(obj).filter_by(tag_name=condition).first()
        return ret

    def remove_data_by_id(self, obj, condition):
        ret = self.session.query(obj).filter_by(id=condition).first()
        self.session.delete(ret)

    def roll_back(self):
        self.session.roolback()

    def clear_buffer(self):
        self.engine.dispose()

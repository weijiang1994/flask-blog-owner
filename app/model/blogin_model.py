# coding: utf-8
from sqlalchemy import Column, DateTime, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Gallery(Base):
    __tablename__ = 'gallery'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    photo_title = Column(String(255), nullable=False)
    photo_path = Column(String(255), nullable=False)
    photo_desc = Column(String(512))
    create_time = Column(DateTime)
    delete_flag = Column(INTEGER(11))
    private_flag = Column(INTEGER(11))


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(String(40), primary_key=True)
    user_name = Column(String(255), nullable=False, comment='administrator account')
    password = Column(String(255), comment='administrator password with md5 encryption algorithm')


class Timeline(Base):
    __tablename__ = 'timeline'
    id = Column(String(40), primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(1024), nullable=False)
    time = Column(DateTime)


class BlogType(Base):
    __tablename__ = 'blog_type'
    id = Column(String(40), primary_key=True)
    type_name = Column(String(40), nullable=False)
    create_time = Column(DateTime)
    blog_count = Column(INTEGER(11), nullable=False, server_default=text("0"))
    description = Column(String(1024), nullable=False)


class Article(Base):
    __tablename__ = 'article'

    id = Column(String(40), primary_key=True, server_default=text("''"), comment='article id')
    title = Column(String(255), nullable=False, server_default=text("''"), comment='article title')
    type = Column(INTEGER(11), nullable=False, comment='article type')
    img = Column(String(255), nullable=False, comment='article preview image')
    brief_content = Column(String(255), nullable=False, server_default=text("''"), comment='article abstract')
    content = Column(Text, nullable=False, comment='article content')
    is_private = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='is private ? 0:no 1:yes')
    create_time = Column(DateTime, comment='article publish time')
    update_time = Column(DateTime, comment='modify this article time')
    read_times = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='this article read times')
    delete_flag = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='is delete? 0:no 1:yes')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(String(40), primary_key=True, server_default=text("''"), comment='comment id')
    article_id = Column(String(40), nullable=False, server_default=text("''"), comment='article id')
    parent_id = Column(String(40), nullable=False, server_default=text("''"), comment='comment and reply relationship')
    comment_time = Column(DateTime, comment='comment time')
    comment_content = Column(String(255), nullable=False, server_default=text("''"), comment='comment content')
    is_read = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='comment have read? 0:no 1:yes')
    delete_flag = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='comment have delete? 0:no '
                                                                                        '1:yes')

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

    id = Column(INTEGER, primary_key=True, nullable=False, comment='comment id', autoincrement=True)
    article_id = Column(String(40), nullable=False, server_default=text("''"), comment='article id')
    parent_id = Column(INTEGER, comment='comment and reply relationship')
    create_u_id = Column(INTEGER, nullable=False, comment='comment create user')
    comment_time = Column(DateTime, comment='comment time')
    comment_content = Column(String(255), nullable=False, server_default=text("''"), comment='comment content')
    delete_flag = Column(INTEGER, nullable=False, comment='comment have delete? 0:no 1:yes')


class Notification(Base):
    __tablename__ = 'notification'
    id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    create_u = Column(INTEGER, nullable=False)
    receive_u = Column(INTEGER, nullable=False)
    comment_id = Column(INTEGER)
    create_time = Column(DateTime)
    readed = Column(INTEGER, nullable=False, comment='is read? 0 no 1 yes')


class PhotoTag(Base):
    __tablename__ = 'photo_tag'
    id = Column(INTEGER, autoincrement=True, primary_key=True, comment='tag id')
    tag_name = Column(String(40), default='', comment='photo tag name')
    photo_counts = Column(INTEGER(11), default=0, comment='bellow this tag photo"s counts')
    create_time = Column(DateTime, comment='this tag create time')
    delete_flag = Column(INTEGER, default=0, comment='delete tag')


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(INTEGER, autoincrement=True, primary_key=True, comment='tags id')
    tag_id = Column(INTEGER, nullable=False, default=0)
    photo_id = Column(String(40), nullable=False, default='')
    create_time = Column(DateTime)


class Users(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, autoincrement=True, primary_key=True, comment='user id')
    email = Column(String(40), nullable=False, default='', comment='register email')
    username = Column(String(40), nullable=False, default='', comment='register username')
    password = Column(String(40), nullable=False, default='', comment='register user password')
    create_time = Column(DateTime)
    delete_flag = Column(INTEGER, default=0)
    avatar = Column(String(128), nullable=False, default='')
    website = Column(String(128), nullable=True, default='')


class LoginLog(Base):
    __tablename__ = 'login_log'

    id = Column(INTEGER, autoincrement=True, primary_key=True, comment='login log id')
    user_id = Column(INTEGER, nullable=False, comment='login user id')
    login_time = Column(DateTime)
    login_ip = Column(String(128), default='')


class Likes(Base):
    __tablename__ = 'likes'

    id = Column(INTEGER, autoincrement=True, primary_key=True, comment='likes id')
    photo_id = Column(String(40), nullable=False, default="''", comment='photo id')
    like_counts = Column(INTEGER, nullable=False, default=1, comment='photo like counts')


class LikePhoto(Base):
    __tablename__ = 'like_photo'

    id = Column(INTEGER, autoincrement=True, primary_key=True, comment='like photo id')
    photo_id = Column(String(40), nullable=False, default="''", comment='like photo id')
    like_user_id = Column(INTEGER, nullable=False, comment='like photo user id')
    like_time = Column(DateTime, nullable=False)
    delete_flag = Column(INTEGER, nullable=False, default=0, comment='like photo delete flag')

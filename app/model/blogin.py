# coding:   utf-8
from sqlalchemy import Column, DateTime, String, text, BIGINT
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(String(40), primary_key=True)
    article_id = Column(String(40), nullable=False)
    comment_publish_time = Column(DateTime, nullable=False)
    have_read = Column(INTEGER(11), nullable=False)
    negative_type = Column(INTEGER(11))
    parent_id = Column(String(40), nullable=False, server_default=text("''"))
    delete_flag = Column(INTEGER(11), server_default=text("0"))


class PrimaryBlogInfo(Base):
    __tablename__ = 'primary_blog_info'

    id = Column(String(35), primary_key=True)
    type = Column(INTEGER(11), server_default=text("0"), comment='博客的类型')
    title = Column(String(255), nullable=False, server_default=text("''"), comment='博客的标题')
    preview_img_path = Column(String(255), nullable=False, server_default=text("''"))
    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime)
    private = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='博客是否为私有')
    preview_content = Column(String(255))
    read_times = Column(BIGINT, nullable=False, server_default=text("0"))

    def __repr__(self):
        return str([self.id, self.type, self.title, self.preview_img_path, self.create_date, self.update_date,
                    self.private, self.preview_content, self.read_times])


class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(String(40), primary_key=True, server_default=text("''"))
    role = Column(INTEGER(11), server_default=text("0"), comment='用户角色目前只包含 0:系统管理员角色')
    username = Column(String(40), server_default=text("''"), comment='用户名')
    password = Column(String(255), server_default=text("''"), comment='用户密码')
    create_time = Column(DateTime, comment='用户创建时间')
    delete_flag = Column(INTEGER(11), server_default=text("0"), comment='用户删除标记 目前用户不可删除')
    current_log_time = Column(DateTime)
    current_log_ip = Column(String(255), server_default=text("''"), comment='最近登录的IP地址')

    def __repr__(self):
        return str([self.id, self.role, self.username, self.password, self.create_time, self.delete_flag,
                    self.current_log_time, self.current_log_ip])


class VisitStatistic(Base):
    __tablename__ = 'visit_statistics'

    id = Column(String(40), primary_key=True)
    visit_date = Column(DateTime)
    visit_total_times_on_day = Column(INTEGER(11))

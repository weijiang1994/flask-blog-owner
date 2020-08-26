"""
# coding:utf-8
@Time    : 2020/8/26
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : blog_forms
@Software: PyCharm
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SelectField, TextAreaField, FileField, SubmitField
from wtforms.validators import Length, DataRequired

from ...model.blogin_model import BlogType
from ...model.db_operate import DBOperator


class PostForm(FlaskForm):
    title = StringField(u'博客标题', validators=[Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': '输入您的博客标题'})
    blog_type = SelectField(label=u'博客类型',
                            default=0,
                            coerce=int)
    blog_level = SelectField(label=u'博客权限', choices=[(1, '公开'), (2, '私有')], validators=[DataRequired()],
                             default=1, coerce=int)
    brief_content = TextAreaField(u'博客简介', validators=[DataRequired()])
    blog_img_file = FileField(label=u'博客示例图',
                              validators=[FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                              render_kw={'value': "上传", 'class': 'btn btn-default'})
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField(u'发布博客')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        db = DBOperator()
        ret = db.query_all(BlogType)
        choices = [(i[0], i[1].type_name) for i in zip(range(len(ret)), ret)]
        db.clear_buffer()
        del db
        self.blog_type.choices = choices

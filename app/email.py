"""
# coding:utf-8
@Time    : 2020/9/17
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : email
@Software: PyCharm
"""
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app.extension import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(to_email, subject, template, **kwargs):
    message = Message(current_app.config['BLOGIN_MAIL_SUBJECT_PRE'] + subject, recipients=[to_email],
                      sender=current_app.config['MAIL_USERNAME'])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    th_send = Thread(target=_send_async_mail, args=(app, message))
    th_send.start()
    return th_send


def send_confirm_email(user, token, to=None):
    send_mail(subject='Register Confirm', to_email=to or user.email, template='email/confirm', user=user, token=token)


def send_verify_code(to_email, **kwargs):
    msg = Message(sender=current_app.config['MAIL_USERNAME'], recipients=[to_email],
                  subject=current_app.config['BLOGIN_MAIL_SUBJECT_PRE'] + '密码修改')
    msg.body = render_template('email/verifyCode.txt', **kwargs)
    msg.html = render_template('email/verifyCode.html', **kwargs)
    app = current_app._get_current_object()
    th_send = Thread(target=_send_async_mail, args=(app, msg))
    th_send.start()
    return th_send

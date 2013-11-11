# -*- coding:utf-8 -*- 
"""
    author sarike@timefly.cn
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from tornado import template


def _get_template_path():
    sep = os.path.sep
    altsep = os.path.altsep or '\\'
    file_path = __file__
    if altsep in __file__:
        file_path = __file__.replace(altsep, sep)
    tpl_path_slice = file_path.split(sep)
    tpl_path_slice.pop()
    tpl_path_slice.append('email_templates')
    return '/'.join(tpl_path_slice)


loader = template.Loader(_get_template_path())


def get_email_content(template_file, **kwargs):
    return loader.load(template_file).generate(**kwargs)


def send_mail(to, subject, text,
              smtp=None,
              account=None,
              password=None):

    assert type(to) == list

    _account = account or __conf__.SMTP_FROM
    frm = '回归线<%s>' % _account
    msg = MIMEMultipart()
    msg['From'] = frm
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text, 'html', _charset='UTF-8'))

    try:
        _port = 25
        if __conf__.SMTP_PORT:
            _port = int(__conf__.SMTP_PORT)

        auth_info = {'smtp': smtp or __conf__.SMTP_HOST, 'user': _account,
                     'password': password or __conf__.SMTP_PASSWORD}
        smtp = smtplib.SMTP(auth_info['smtp'], _port, timeout=20)
        smtp.login(auth_info['user'], auth_info['password'])
        smtp.sendmail(frm, to, msg.as_string())
        smtp.quit()
        return True
    except Exception:
        return False

if __name__ == "__main__":
    send_mail(["cmaj135@gmail.com"], "Test Subject", "Test Message")

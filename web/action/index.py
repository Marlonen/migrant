# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    migrant 前端展示公共页面
"""
from kpages import url
from kpages.context import get_context
from utility import BaseHandler


@url(r'/?')
class Index(BaseHandler):
    def get(self):
        self.render('action/index.html')


@url(r'/login?')
class Login(BaseHandler):
    def get(self):
        self.render('action/login.html')


@url(r'/logout?')
class Logout(BaseHandler):
    def get(self):
        self.clear_cookie('uid')
        self.clear_cookie('city')
        self.redirect('/')


@url(r'/profile?')
class Profile(BaseHandler):
    def get(self):
        self.render('action/profile.html')


@url(r'/setpwd?')
class SetPwd(BaseHandler):
    def get(self):
        self.render('action/setpwd.html')


@url(r'/forgot_password?')
class ForgotPassword(BaseHandler):
    def get(self):
        key = self.get_argument('key', None)
        kwargs = {
            'key': None,
            'expired': False
        }
        template_file = 'action/forget_password.html'
        if not key:
            self.render(template_file, **kwargs)
        else:
            with get_context() as context:
                redis = context.get_redis()
                username = redis.get(key)
                if username:
                    kwargs.update(key=key)
                    self.render(template_file, **kwargs)
                else:
                    kwargs.update(expired=True)
                    self.render(template_file, **kwargs)
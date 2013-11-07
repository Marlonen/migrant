# -*- coding:utf-8 -*- 
"""
    account action 
    author comger@gmail.com
"""
import json
from kpages import url
from utility import RestfulHandler,BaseHandler

from logic.utility import *
from logic.account import add,login,TName as T_ACCOUNT,auth_login, INIT, reset_pwd
from logic.city import TName as T_CITY
from logic.openfireusers import add as openfire_add

@url(r'/m/account/login')
class LoginHandler(BaseHandler):
    def post(self):
        r,v = login(self.get_argument('username'),self.get_argument('password'))
        print r,v
        if r:
            self.set_secure_cookie('uid',v['_id'])
            self.set_secure_cookie('nickname', v['nickname'])
            self.set_secure_cookie('username', v['username'])
            del v['password']
            self.write(dict(status = r, data = v))
        else: 
            self.write(dict(status = r, errormsg = "登录失败"))


@url(r'/m/account/join')
class RegisterHandler(BaseHandler):

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        result, value = add(username, password, self.get_argument('city', None), status=INIT)

        if result:
            if '@' in username:
                username, email_host = username.split('@')
            openfire_add(username, password, username)

            self.set_secure_cookie('uid', value['_id'])
            self.set_secure_cookie('nickname', value['username'])

            del value['password']

        self.write(dict(status=result, data=value))


@url(r'/m/auth/login')
class AuthLoginHandler(BaseHandler):
    def post(self):
        r,v = auth_login(self.get_argument('site'),self.get_argument('otherid'),self.get_argument('name'))
        if r:
            self.set_secure_cookie('uid',v['_id'])
            del v['password']
            del v['status']

        self.write(dict(status = r, data = v))


@url(r'/m/account/update')
class UpdateHandler(RestfulHandler):
    def post(self):
        self.get()

    def get(self):
        args = {
            'mobile': self.get_argument('mobile', None),
            'labels': self.get_arguments('labels'),
            'profession': self.get_arguments('profession'),
            'intro': self.get_arguments('intro'),
            'skill': self.get_arguments('skill'),
            'nickname': self.get_argument('nickname'),
            'parent_city': self.get_argument('parent_city', None),
            'city': self.get_argument('city', None)
        }
        r, v = m_update(T_ACCOUNT, self.uid, **args)
        self.write(dict(status=r, data=v))


@url(r'/m/account/resetpwd')
@url(r'/m/account/resetpwd/(.*)')
class ResetPwdHandler(RestfulHandler):
    def post(self, _id=None):
        old_password = self.get_argument('password')
        new_password = self.get_argument('new_password')
        confirm_password = self.get_argument('confirm_password')

        if new_password == confirm_password:
            r, v = reset_pwd(_id or self.uid, old_password, new_password)
            self.write(dict(status=r, data=v))
        else:
            self.write(dict(status=False, data='DIFFERENT_PWD'))


@url(r'/m/account/info')
@url(r'/m/account/info/(.*)')
class InfoHandler(RestfulHandler):
    def get(self, _id=None):
        r, v = m_info(T_ACCOUNT, _id or self.uid)
        if not r:
            return self.write(dict(status=r, data=v))

        if v and v.get('parent_city', None):
            cr, cv = m_info(T_CITY, v['parent_city'])
            v['parent_city'] = cv['name']
            v['parent_city_id'] = cv['_id']

        if v and v.get('city', None):
            cr, cv = m_info(T_CITY, v['city'])
            v['city'] = cv['name']
            v['city_id'] = cv['_id']

        if v and v.get('to_city', None):
            cr, cv = m_info(T_CITY, v['to_city'])
            v['to_city'] = cv['name']
            v['to_city_id'] = cv['_id']

        del v['password']

        self.write(dict(status=True, data=v))

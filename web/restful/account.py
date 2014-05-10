# -*- coding:utf-8 -*- 
"""
    account action 
    author comger@gmail.com
"""
import json
from kpages import url
from kpages.model import ModelMaster
import tornado
from utility import RestfulHandler,BaseHandler

from logic.utility import *
from logic.account import INIT, ACTIVATED, IDENTIFIED
from logic.city import TName as T_CITY
from logic.label import add as addlabel
from logic.openfireusers import add as openfire_add
from utils.string_utils import random_key


AModel = ModelMaster()('AccountModel')

@url(r'/m/account/login')
class LoginHandler(BaseHandler):
    def post(self):
        r, v = AModel.login(self.get_argument('username'), self.get_argument('password'))

        if r:
            self.set_secure_cookie('uid', v['_id'])
            self.set_secure_cookie('nickname', v.get('nickname', v['username']))
            if v.get('isadmin') == True:
                self.set_secure_cookie('__ADMIN_USER_ID', v['_id'])
            
            del v['password']
            self.write(dict(status=r, data=v))
        else: 
            self.write(dict(status=False, data=v))


@url(r'/m/account/join')
class RegisterHandler(BaseHandler):

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        result, value = AModel.add(username, password, 
                    self.get_argument('city', None), status=INIT)
        '''
        if result:
            if '@' in username:
                username, email_host = username.split('@')
            openfire_add(username, password, username)
        '''
        self.write(dict(status=result, data=value))


@url(r'/m/auth/login')
class AuthLoginHandler(BaseHandler):
    def post(self):
        r,v = AModel.auth_login(self.get_argument('site'),
                self.get_argument('otherid'),self.get_argument('name'))
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
            'intro': self.get_argument('intro'),
            'skill': self.get_arguments('skill'),
            'nickname': self.get_argument('nickname'),
            'parent_city': self.get_argument('parent_city', None),
            'city': self.get_argument('city', None)
        }

        uv = AModel.info(self.uid)
        for i in args.get('profession'):
            if i and not i in uv.get('profession',()):
                addlabel(0,i)

        for i in args.get('skill'):
            if i and not i in uv.get('skill',()):
                addlabel(1,i)

        for i in args.get('labels'):
            if i and not i in uv.get('labels',()):
                addlabel(2,i)

        v = AModel.update(self.uid, **args)
        self.write(dict(status=True, data=v))


@url(r'/m/account/resetpwd')
@url(r'/m/account/resetpwd/(.*)')
class ResetPwdHandler(RestfulHandler):
    def post(self, _id=None):
        old_password = self.get_argument('password')
        new_password = self.get_argument('new_password')
        confirm_password = self.get_argument('confirm_password')

        if new_password == confirm_password:
            r, v = AModel.reset_pwd(_id or self.uid, old_password, new_password)
            self.write(dict(status=r, data=v))
        else:
            self.write(dict(status=False, data='DIFFERENT_PWD'))


@url(r'/m/account/forgot_password')
class ForgetPwdHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        username = self.get_argument('username', None)
        r, v = AModel.forgot_pwd(username,self.request.host)
        self.write(dict(status=r, data=v))
        self.finish()


@url(r'/m/account/reset_forgotten_password')
class UpdateForgottenPwdHandler(BaseHandler):
    def post(self):
        key = self.get_argument('key')
        new_password = self.get_argument('new_password')
        confirm_password = self.get_argument('confirm_password')
        print key ,new_password, confirm_password
        if new_password != confirm_password:
            self.write(dict(status=False, data='两次输入的密码不一致'))
        else:
            r, v = AModel.reset_forgotten_password(key, new_password)
            self.write(dict(status=r, data=v))


@url(r'/m/account/info')
@url(r'/m/account/info/(.*)')
class InfoHandler(RestfulHandler):
    def get(self, _id=None):

        v = AModel.info(_id or self.uid)
        if not v:
            return self.write(dict(status=False, data=v))

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

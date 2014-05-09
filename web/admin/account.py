#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    account action
    author comger@gmail.com
"""

from kpages import url
from kpages.model import ModelMaster
from utility import ActionHandler
from logic.utility import m_update,m_del,m_info,m_exists

AModel = ModelMaster()('AccountModel')

@url(r"/admin/?")
class AdminHandler(ActionHandler):
    def get(self):
        self.render('admin/index.html')


@url(r"/admin/help")
class HelpHandler(ActionHandler):
    def get(self):
        self.render('admin/help.html')


@url(r"/admin/account")
class AccountHandler(ActionHandler):
    def get(self):
        since = self.get_argument("since", None)
        key = self.get_argument("key", None)
        cond = {}
        if key:
            cond = {'username':{'$regex':key}}
        v = AModel.page(since,**cond)

        self.render("admin/account.html", data = v)


@url(r"/admin/account/save")
class AccountSaveHandler(ActionHandler):
    def post(self):
        email = self.get_argument("email", None)
        tel = self.get_argument("tel", '')
        city = self.get_argument("city", '')
        isadmin = bool(self.get_argument('isadmin','True'))

        cond = dict(email = email, tel = tel, isadmin = isadmin,city=city)
        try:
            data = self._get_postdata()
            data.update(cond)
            v = AModel.save(data)
            self.redirect('/admin/account')
        except Exception as e:
            self.write(e.message) 

    def get(self):
        _id = self.get_argument("id", None)
        info = {}
        if _id:
            info = AModel.info(_id)

        self.render('admin/accountinfo.html', info = info)

@url(r"/admin/account/delete")
class AccountDeleteHandler(ActionHandler):
    def post(self):
        _id = self.get_argument("id", None)
        r = AModel.remove(_id)
        self.write(dict(status = r))



@url(r"/admin/login")
class LoginHandler(ActionHandler):
    def get(self):
        self.render('admin/login.html',errormsg = '',next = self.get_argument('next','/admin'))

    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        nexturl = self.get_argument("next",'/admin')

        r,v = AModel.login(username, password,True)

        if r:
            self.set_secure_cookie("admin_user_name", username)
            self.set_secure_cookie(self._Admin_user_id, v['_id'])
            self.write(dict(status=r,next=nexturl))
        else:
            self.write(dict(status=r,message=v))


@url(r"/admin/account/setpassword")
class SetPwdHandler(ActionHandler):
    def get(self):
        self.render('admin/setpassword.html',errormsg = '')

    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("oldpassword", None)
        newpassword = self.get_argument("password", None)

        r,v = AModel.login(username, password,True)
        if r:
            r,v = AModel.update(v['_id'],password=newpassword)
            v = '密码修改成功'
        else:
            v = '密码错误'

        self.render('admin/setpassword.html',errormsg = v)    

@url(r"/admin/logout")
class LogoutHandler(ActionHandler):
    def get(self):
        self.signout_admin()

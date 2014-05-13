#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    account action
    author comger@gmail.com
"""

from kpages import url,not_empty
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
        page = int(self.get_argument("page", 0))
        key = self.get_argument("key", None)
        cond = {}
        if key:
            cond = {'username':{'$regex':key}}

        v = AModel.page(page=page,**cond)
        npage = AModel.count(**cond)/10
        self.render("admin/userlist.html", data = v, page=page, npage=npage)


@url(r"/admin/account/update")
class AccountUpdate(ActionHandler):
    def post(self):
        mobile = self.get_argument('mobile')
        nickname = self.get_argument('nickname')
        isadmin = bool(self.get_argument('isadmin'))

        _id = self.get_argument('_id')
        try:
            r = AModel.update(_id, mobile=mobile,nickname=nickname,
                            isadmin=isadmin)
            
            self.write(dict(status=r))
        except Exception as e:
            self.write(dict(status=False, errmsg = e.message))

    def get(self):
        _id = self.get_argument("_id", None)
        not_empty(_id)
        info = AModel.info(_id)
        self.write(dict(status=True, data=info))


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

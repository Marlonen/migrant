# -*- coding:utf-8 -*-
"""
    author comger@gmail.com
"""
from bson import ObjectId
from kpages import url, app_path, reg_ui_method,not_empty
from tornado.web import UIModule
from tornado import template


class BaseUIModule(UIModule):
    @classmethod
    def to_string(cls):
        funargs = cls.render.func_code.co_varnames
        count = cls.render.func_code.co_argcount
        
        name = '{0}.{1}{2}'.format(cls.__module__ ,cls.__name__,list(funargs[1:count]))
        name = name.replace('.','_')
        name = name.replace("'",'')
        name = name.replace('[','(')
        name = name.replace(']',')')

        return name


class PageHandler(BaseUIModule):
    """
    分页UI
    """
    def render(self,current,npage,url=''):
        return self.render_string('admin/m_page.html',page=current,npage=npage,pageurl=url)


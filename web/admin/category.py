#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    category action
    author comger@gmail.com
"""

from kpages import url
from utility import ActionHandler
from logic.category import TName as T_CATEGORY,CategoryModel
from logic.utility import m_page,m_del,m_info,m_update,m_exists

@url(r"/admin/category/find")
class CategoryFindHandler(ActionHandler):
    def get(self):
        groupid = self.get_argument('groupid',None)
        cond = dict(groupid = groupid)
        r,cates = m_page(T_CATEGORY,**cond)
        self.write(dict(status = r,categorys = cates))


@url(r"/admin/category")
class CategoryHandler(ActionHandler):
    def get(self):
        since = self.get_argument("since", None)
        cond = {}
        r,cates = m_page(T_CATEGORY,**cond)
        self.render("admin/category.html", data = cates) 



@url(r'/admin/category/info/(.*)')
class CategoryInfoHandler(ActionHandler):
    def get(self,_id):
        r,info = m_info(T_CATEGORY,_id)
        self.write(dict(status =r,data = info))


@url(r"/admin/category/save")
class CategorySaveHandler(ActionHandler,CategoryModel):
    def post(self):
        try:
            data = self._get_postdata()
            r = m_exists(T_CATEGORY,listname=data['listname'])
            if not r:
                r, data = self._save(data)
            else:
                r, data = False,"已存在此域名"

            self.write(dict(status=r,data=data))
        except Exception as e:
            self.write(dict(status=False,data=e.message))

    def get(self):
        _id = self.get_argument("id", None)
        info = {}
        if _id:
            r,info = m_info(T_CATEGORY,_id)

        self.render('admin/categoryinfo.html', info = info)

@url(r"/admin/category/delete")
class CategoryDeleteHandler(ActionHandler):
    def post(self):
        _id = self.get_argument("id", None)
        r,v = m_del(T_CATEGORY,_id)
        self.write(dict(status = r,data = v))






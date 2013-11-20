#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    servercity action
    author comger@gmail.com
"""

from kpages import url
from utility import ActionHandler
from logic.servercity import TName as T_Servercity,CityModel
from logic.utility import m_page,m_del,m_info,m_update,m_exists

@url(r"/admin/servercity/find")
class ServerCityFindHandler(ActionHandler):
    def get(self):
        r,cates = m_page(T_Servercity)
        self.write(dict(status = r,servercitys = cates))


@url(r"/admin/servercity")
class ServerCityHandler(ActionHandler):
    def get(self):
        since = self.get_argument("since", None)
        cond = {}
        r,cates = m_page(T_Servercity,**cond)
        self.render("admin/servercity.html", data = cates) 



@url(r'/admin/servercity/info/(.*)')
class ServerCityInfoHandler(ActionHandler):
    def get(self,_id):
        r,info = m_info(T_Servercity,_id)
        self.write(dict(status =r,data = info))


@url(r"/admin/servercity/save")
class ServerCitySaveHandler(ActionHandler,CityModel):
    def post(self):
        try:
            data = self._get_postdata()
            r = m_exists(T_Servercity,listname=data['listname'])
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
            r,info = m_info(T_Servercity,_id)

        self.render('admin/servercityinfo.html', info = info)

@url(r"/admin/servercity/delete")
class ServerCityDeleteHandler(ActionHandler):
    def post(self):
        _id = self.get_argument("id", None)
        r,v = m_del(T_Servercity,_id)
        self.write(dict(status = r,data = v))






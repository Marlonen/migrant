#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    news action
    author comger@gmail.com
"""

from kpages import url
from utility import ActionHandler
from logic.utility import m_page,m_del,m_info,m_update,m_exists
from logic.news import TName as TNews,NewsModel

@url(r"/admin/news?")
class NewsHandler(ActionHandler):
    def get(self):
        since = self.get_argument("since", None)
        cond = {}
        r,cates = m_page(TNews,since=since, **cond)
        self.render("admin/news.html", data = cates) 



@url(r'/admin/news/info/(.*)')
class CategoryInfoHandler(ActionHandler):
    def get(self,_id):
        r,info = m_info(TNews,_id)
        self.write(dict(status =r,data = info))


@url(r"/admin/news/save")
class NewsSaveHandler(ActionHandler,NewsModel):
    def post(self):
        try:
            data = self._get_postdata()
            r, data = self._save(data)

            self.write(dict(status=r,data=data))
        except Exception as e:
            self.write(dict(status=False,data=e.message))

    def get(self):
        _id = self.get_argument("id", None)
        info = {}
        if _id:
            r,info = m_info(TNews,_id)

        self.render('admin/newsinfo.html', info = info)

@url(r"/admin/news/delete")
class NewsDeleteHandler(ActionHandler):
    def post(self):
        _id = self.get_argument("id", None)
        r,v = m_del(TNews,_id)
        self.write(dict(status = r,data = v))






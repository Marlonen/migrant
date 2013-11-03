# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    migrant 前端展示公共页面
"""
from kpages import url
from utility import BaseHandler


@url(r'/news?')
class News(BaseHandler):
    def get(self):
        self.render('action/news.html')


@url(r'/news/info/(.*)')
class NewsInfo(BaseHandler):
    def get(self,_id=None):
        self.render('action/newsinfo.html')

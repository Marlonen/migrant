# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    migrant 前端展示公共页面
"""
from kpages import url
from utility import BaseHandler
from logic.news import NewsModel

@url(r'/news?')
class News(BaseHandler):
    def get(self):
        self.render('action/news.html')


@url(r'/news/info/(.*)')
class NewsInfo(BaseHandler):
    def get(self,_id=None):
        self.render('action/newsinfo.html')

@url(r'/news/create')
class CreateNews(BaseHandler,NewsModel):
    def post(self):
        try:
            data = self._get_postdata()
            _id = self._save(data)
            self.write(dict(status=True,data=_id)) 
        except Exception as e:
            self.write(e.message)

    def get(self):
        self.render('action/newssave.html')

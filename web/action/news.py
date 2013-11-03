# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    migrant 前端展示公共页面
"""
from kpages import url
from utility import BaseHandler
from logic.news import NewsModel
from logic.category import TName as T_Category
from logic.utility import m_page

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
            data = self._get_postdata(author=self.uid)
            r,v = self._save(data)
            self.write(dict(status=r,data=v)) 
        except Exception as e:
            self.write(e.message)

    def get(self):
        self.labels = ['码农'.decode('utf-8'),'码码代']
        r,self.categorys = m_page(T_Category,size=10)        
        print self.categorys 
        self.render('action/newssave.html')



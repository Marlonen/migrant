# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    migrant 前端展示公共页面
"""
import datetime
import re
from kpages import url
from utility import BaseHandler
from logic.news import NewsModel,hot,TName as TNews
from logic.category import TName as T_Category
from logic.account import TName as T_Account
from logic.utility import m_page,m_info
from logic.label import add as addlabel

strip_tag_pat=re.compile('</?\w+[^>]*>')

@url(r'/news?')
class News(BaseHandler):
    def get(self):
        self.oneday = hot(5,1)
        self.weeknews = hot(5,7)
        self.monthnews = hot(5,30)
        r,self.categorys = m_page(T_Category,size=10)        
        news = {}
        for cate in self.categorys:
            r,news[cate.get('listname')] = m_page(TNews,category=cate.get('listname'))
        
        
        self.news = news
        self.render('action/news.html')


@url(r'/news/info/(.*)')
class NewsInfo(BaseHandler):
    def get(self,_id=None):
        r,v = m_info(TNews,_id)
        
        cr,cv = m_info(T_Category,v['category'],key='listname')
        v['categoryname'] = cv['name']
        
        
        ur,uv = m_info(T_Account,v['author'])
        v['authorname'] = uv.get('nickname',None) or uv['username']
        
        self.render('action/newsinfo.html',info = v)

@url(r'/news/create')
class CreateNews(BaseHandler,NewsModel):
    def post(self):
        try:
            addon = datetime.datetime.now()
            data = self._get_postdata(addon=addon)
            intro = re.sub(strip_tag_pat,' ',data.get('body',''))
            data['intro'] = intro[0:100]
            r,v = self._save(data)
            for i in data.get('labels',()):
                if i:
                    addlabel(3,i)

            self.write(dict(status=r,data=v)) 
        except Exception as e:
            self.write(dict(status=False,data=e.message))

    def get(self):
        r,self.categorys = m_page(T_Category,size=10)        
        self.render('action/newssave.html')



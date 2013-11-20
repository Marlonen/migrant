# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    comment 接口
"""
import datetime
from kpages import url
from utility import BaseHandler
from logic.account import TName as T_Account
from logic.news import TName as TNews
from logic.comment import CommentModel,TName as TComment
from logic.utility import m_page,m_info

@url(r'/m/comment/list/(.*)')
class CommentList(BaseHandler):
    def get(self, news_id):
        since = self.get_argument('since',None)
        r,data = m_page(TComment,since=since, news_id=news_id)
        for item in data:
            r,v = m_info(T_Account,item['author'])
            if r and v:
                item['authorname'] =v.get('nickname', v['username'])
        
        self.write(dict(status=r, data=data))


@url(r'/m/comment/post')
class CreateComment(BaseHandler,CommentModel):
    def post(self):
        try:
            data = self._get_postdata()
            r,v = self._save(data)
            self.write(dict(status=r,data=v)) 
        except Exception as e:
            self.write(dict(status=False,data=e.message))




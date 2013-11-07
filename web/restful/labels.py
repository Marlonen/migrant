# -*- coding:utf-8 -*- 

"""
    comment action 
    author comger@gmail.com
"""
import json
from tornado.web import RequestHandler
from kpages import url
from utility import RestfulHandler
from logic.utility import m_page
from logic.label import add,suggest

@url(r'/m/label/suggest/(.*)')
class SuggestLabel(RestfulHandler):
    def get(self, category=None):
        key = self.get_argument('key',None)
        rs = suggest(int(category),key=key)
        arr = [ item['name'] for item in rs]
        self.write(dict(status=True,data=arr))


@url(r'/m/label/add')
class AddLabel(RestfulHandler):
    def post(self):
       name = self.get_argument('name',None)
       category = int(self.get_argument('category','0'))
       r,v = add(category, name)
       self.write(dict(status=r, data=v))


@url(r'/m/label/list/(.*)')
class ListLable(RestfulHandler):
    def get(self, category=None):
        rs = suggest(int(category))
        self.write(dict(status=True, data=rs))

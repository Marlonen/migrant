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

@url(r'/m/label/suggest/(.*)')
class SuggestLabel(RequestHandler):
    def post(self, category=None):
        arr = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Dakota","North Carolina","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
        #self.write(json.dumps(arr))
        arr = ['码爱','码农','码工要']
        self.write(dict(status=True,data=arr))

@url(r'/m/label/add')
class AddLabel(RestfulHandler):
    def post(self):
        pass


@url(r'/m/label/list/(.*)')
class ListLable(RestfulHandler):
    def get(self, category=None):
        pass


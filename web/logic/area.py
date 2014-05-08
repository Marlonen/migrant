#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    开通城市管理逻辑
"""

from kpages import not_empty,get_context,mongo_conv
from kpages.model import *

from pinying import get_pinyin

TName = 'serverarea'

class AreaModel(Model):
    _name = TName
    _fields = dict(
        name = CharField(required=True),
        listname = CharField(),
        intro = CharField(),
        order = IntField(),
        cover = CharField(),
        coverThumbnail = CharField(),
    )

    def info_city_listname(self, listname):
        ''' city info by listname '''
        not_empty(listname)
        try:
            return self._coll().info(listname, key='listname')
        except Exception as e:
            print e 
            return None
    

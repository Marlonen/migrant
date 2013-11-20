#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    开通城市管理逻辑
"""

from kpages import not_empty,get_context,mongo_conv
from kpages.model import *

from pinying import get_pinyin
from utility import BaseModel,m_update,m_del,m_page,m_exists

TName = 'servercity'
Tb = lambda :get_context().get_mongo()[TName]

class CityModel(BaseModel):
    _name = TName
    _fields = dict(
        name = CharField(required=True),
        listname = CharField(required=True),
        order = IntField(),
    )



def info_city_listname(listname):
    ''' city info by listname '''
    not_empty(listname)
    try:
        val = Tb().find_one(dict(listname = listname))
        val["_id"] = str(val['_id'])
        return val
    
    except Exception as e:
        return None
    

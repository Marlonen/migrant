#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    news 管理逻辑
"""

from kpages import not_empty,get_context,mongo_conv
from kpages.model import *

from pinying import get_pinyin
from utility import BaseModel,m_update,m_del,m_page,m_exists

TName = 'news'
Tb = lambda :get_context().get_mongo()[TName]

class NewsModel(BaseModel):
    _name = TName

    title = CharField(required=True)
    body = CharField()
    category = CharField(required=True)
    author = CharField(required=True)
    labels = ListField(datatype=CharField)


def hot(top, days=1):
    """
        dtype : day, week, month 
        get top hot news by dtype
    """
    #TODO
    pass



    

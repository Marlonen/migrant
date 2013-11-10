#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    comment 管理逻辑
"""
import datetime
from bson import ObjectId
from kpages import not_empty,get_context,mongo_conv
from kpages.model import *

from utility import BaseModel,m_update,m_del,m_page,m_exists

TName = 'comment'
Tb = lambda :get_context().get_mongo()[TName]

class CommentModel(BaseModel):
    _name = TName

    body = CharField()
    addon = DatetimeField()
    news_id = CharField(required=True)
    ref = CharField()
    author = CharField(required=True)
 

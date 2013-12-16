#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    project 管理逻辑
"""
import datetime
from bson import ObjectId
from kpages import not_empty,get_context,mongo_conv
from kpages.model import *

from utility import BaseModel,m_update,m_del,m_page,m_exists

TName = 'project'
Tb = lambda :get_context().get_mongo()[TName]

class ProjectModel(BaseModel):
    _name = TName
    _fields = dict(
        name = CharField(required=True),
        description = CharField(),
        advantage = CharField(),
        partner = ListField(datatype=Charfild),
        author = CharField(required=True),
        city = CharField(required=True),
        status = IntField(initial = 0)
    )

    

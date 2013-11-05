#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    分类管理逻辑
"""

from kpages import not_empty,get_context,mongo_conv
from kpages.model import *

from utility import BaseModel,m_update,m_del,m_page,m_exists

TName = 'label'
Tb = lambda :get_context().get_mongo()[TName]

class LabelModel(BaseModel):
    _name = TName

    name = CharField(required=True)
    category = IntField(Required=True)


def suggest(category, top=10):
    """
        按热度排序,返回category 分类前top 条记录
    """
    pass



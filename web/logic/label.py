#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    分类管理逻辑
"""

from kpages import not_empty,get_context,mongo_conv
from kpages.model import *

from utility import BaseModel,m_add,m_update,m_del,m_page,m_exists

TName = 'label'
Tb = lambda :get_context().get_mongo()[TName]

class LabelModel(BaseModel):
    _name = TName

    name = CharField(required=True)
    category = IntField(Required=True)


def add(category, name, **kwargs):
    try:
        not_empty(category,name)
        cond = dict(category = category, name=name)
        val = m_exists(TName,**cond)
        if not val:
            #如果不存在此标签 则添加
            cond['usage'] = 1
            cond['hot']  = 0
            r,_id = m_add(TName,cond)
            cond['_id'] = _id
        else:
            cond.update(status={'$ne':-1})
            Tb().update(cond,{'$inc':{'usage':1}})

        return True, cond
    except Exception as e:
        return False,e.message


def suggest(category, top=10):
    """
        按热度排序,返回category 分类前top 条记录
    """
    pass



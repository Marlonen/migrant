# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
"""
from bson import ObjectId
import json
from kpages import LogicContext,reflesh_config
from logic.label import add,TName
from logic.utility import m_del,m_page,m_update,m_exists
from unittest import TestCase


class LabelCase(TestCase):
    def setUp(self):
        pass

    def test_upadte(self):
        label = dict(name='80后',category=1)
        val = m_exists(TName,**label)
        print m_del(TName,val['_id'])

        print add(1,'80后')
        print add(1,'80后')
        print add(1,'80后')

        val = m_exists(TName,**label)
        print val
        assert val['usage'] ==3

        print m_page(TName)
        



# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
"""
from bson import ObjectId
import json
from logic.utility import m_del,m_page,m_update,m_exists
from unittest import TestCase
from logic.news import hot

class NewsCase(TestCase):
    def setUp(self):
        pass

    def test_hot(self):
        print 'one day news'
        print hot(3,1)

        print 
        print
        print 'week hot'
        lst = hot(3,7)
        print len(lst)
        assert len(lst) <=3

        print 
        print
        print 'month hot'
        lst = hot(10,30)
        print len(lst)
        assert len(lst) <=10


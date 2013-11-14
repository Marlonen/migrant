# -*- coding:utf-8 -*- 
"""
    test for spider module
    author comger@gmail.com
"""
import tornado
import urllib2
from unittest import TestCase

class SpiderCase(TestCase):
    
    def setUp(self):
        pass

    def test_getspiders(self):
        pass

    def on_end(self,data):
        print len(data)

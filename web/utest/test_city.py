#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" The city unit test

    @author comger@gmail.com,cmaj135@gmail.com
    @version 1.0
    @date 2013-11-13
"""
import json
from kpages import LogicContext,reflesh_config
from logic.city import add, getList, refresh, CITY_VAL
from logic.utility import m_page, m_update, m_del
from unittest import TestCase


class CityUnitTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """The city unit_test that prepare data

        """
        pass
    def __init__(self,methodName='runTest'):
        TestCase.__init__(self,methodName)
        self.city_name = 'HangZhou'
        self.parent_name = 'ZheJiang'

    def test_add_accuracy1(self):
        ret, entity = add(name=self.city_name,parent=self.parent_name)
        self.assertTrue(ret, msg='the add city must be successful')
        self.assertIsNotNone(entity,msg='the city entity should not be null')
        self.__class__.entity_id = entity['_id']

    def test_add_failure1(self):
        ret,entity = add(name=self.city_name,parent=self.parent_name)
        self.assertFalse(ret,msg='the city has already exist')

    def test_add_failure2(self):
        ret,entity = add(None)
        self.assertFalse(ret,msg='the city name should not be none')

    def test_getList_accuracy1(self):
        lst = getList(self.parent_name)
        self.assertEqual(len(lst),1)

    def test_refresh_accuracy1(self):
        refresh()
        self.assertGreater(len(CITY_VAL),1,msg='at least have one city')

    @classmethod
    def tearDownClass(cls):
        if cls.entity_id:
            m_del('city',cls.entity_id,is_del=True)


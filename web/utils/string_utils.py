# -*- coding:utf-8 -*-
"""
    author sarike@timefly.cn
"""
import string
import random


def random_key():
    return ''.join([random.choice(string.letters) for i in xrange(48)])
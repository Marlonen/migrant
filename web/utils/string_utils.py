# -*- coding:utf-8 -*-
"""
    author sarike@timefly.cn
"""
import string
import random
import hashlib
from kpages import not_empty

def random_key():
    return ''.join([random.choice(string.letters) for i in xrange(48)])

def hashPassword(password):
    """Hash the user password.

    Args:
        password : the user input password.
    Returns:
        the password with md5 hashable

    """
    not_empty(password)
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()
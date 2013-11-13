#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    This is the nose test that can be executed to see unit test result,coverage,etc.

    @author cmaj135@gmail.com
    @version 1.0
    @date 2013-11-13
"""
import nose
from optparse import OptionParser
from kpages import LogicContext, reflesh_config, set_default_encoding


# the default parameters that pass to nose
default_args = ['-w', 'utest/', '--with-coverage', '--cover-tests', '--cover-erase',
                '--cover-package=logic,utils,spiders', '--cover-html', '--cover-html-dir=cover']

def _get_opt():
    """ get the configuration of this app

    the default configuration file is setting.py
    """
    parser = OptionParser("%prog [options]", version="%prog v0.9")
    parser.add_option("--config", dest="config",
                      default='setting.py', help="config for app")
    return parser.parse_args()

if __name__ == "__main__":
    try:
        set_default_encoding()
        opts, args = _get_opt()
        reflesh_config(opts.config)

        with LogicContext():
            nose.run(argv=default_args)

    except KeyboardInterrupt:
        print 'exit nose_test '
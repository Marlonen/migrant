# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    news spider
"""
import tornado
import urllib
from kpages import set_default_encoding
from pyquery import PyQuery as pyq
from tornado import httpclient

def main():
    url = 'http://taiwan.huanqiu.com/news/'
    url = 'http://world.huanqiu.com/observation/'
    url = 'http://china.huanqiu.com/politics/'
    doc = pyq(url=url)
    alist = doc('.pad20 li a')
    for a in alist:
        link = pyq(a).attr('href')
        get_info(link)
        

def get_info(url):
    doc = pyq(url=url)
    params = dict(
        title = doc('h1').text(),
        author = '52847ffb1a7f5a7d80fd1ff7',
        category = 'company',
        city = '51d28ace931e334378000001',
        body = doc('#text').html(),
        labels = '测试',
            )

    body = urllib.urlencode(params)

    def callback(res):
        print 'ok'
        tornado.ioloop.IOLoop.instance().stop()

    http_client = httpclient.AsyncHTTPClient() 
    http_client.fetch('http://www.sos360.com:8888/news/create',callback,method='POST',body=body)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    set_default_encoding()
    main()

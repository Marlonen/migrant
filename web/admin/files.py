#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    server area  action
    author comger@gmail.com
"""
import time
import math
import motor
from functools import partial
from tornado import gen
from tornado.web import RequestHandler
from kpages import url,get_context,ContextHandler
from kpages.model import ModelMaster
from utility import ActionHandler
from logic.pinying import get_pinyin
from logic.files import *

@url(r'/file/(?P<ftype>[0-9A-Za-z-]+)/(?P<fid>[0-9A-Za-z-]+)')
class GetFile(ContextHandler,RequestHandler):
    @gen.coroutine
    def get(self,ftype,fid):
        f = yield gen.Task(get_file,fid,ftype)
        self.set_header('Content-Type', f['contentType'])
        self.write(f['data'])
        self.finish()
    
@url(r'/admin/files/(?P<ftype>[0-9A-Za-z-]+)/(?P<fid>[0-9A-Za-z-]+)')
class DelFile(ActionHandler):
    @gen.coroutine
    def delete(self,ftype,fid):
        if ftype == "image":
            yield gen.Task(del_image,fid)
            self.write(dict(status=True))

@url(r"/admin/files/(?P<ftype>[0-9A-Za-z-]+)/")
class FileList(ActionHandler):
    @gen.coroutine
    def get(self,ftype):
        page = int(self.get_argument('page',0)) 
        size = int(self.get_argument('limit',10))
        lst,count = yield image_page(page,size=size, ftype=ftype)
        file_list = map(partial(conv, table=ftype), lst)
        npage = int(math.ceil((count+1)/size))
        view = self.get_argument('view',None)
        if view == "grid" and ftype == "image":
            grid= self.render_string("admin/filelist/img-grid.html", images=file_list)
            pagniation= self.render_string("admin/filelist/pagination.html", page=page, npage=npage)
            self.write(dict(grid=grid,pagniation=pagniation))
        elif view == 'json':
            self.write({
                'dir':ftype,
                'file_list':file_list,
                'page':page,
                'npage':npage}
                )
        else:
            self.render('admin/files.html')

@url(r"/admin/file/upload")
class FileUpload(ActionHandler):
    @gen.coroutine
    def post(self):
        f = self.request.files['mfile'][0]
        body = f.pop('body')
        filename = f.pop('filename')
        content_type = f.pop('content_type')
        ts = time.time()
        filename = '%d_%s' % (ts,filename)
        ftype = self.get_argument('ftype','image')
        if ftype == 'image':
            fmt = content_type.split('/')[1]
            fid = yield gen.Task(put_image,body,filename,fmt,content_type=content_type)
            val = dict(dir=ftype,error=0,url='/file/image/{0}'.format(fid))
            val.update(thumbnail='/file/thumbnail/{0}'.format(fid))
            self.write(val)
        elif ftype == 'file':
            fid = yield put_file(body,filename, content_type=content_type)
            val = dict(dir=ftype,error=0,url='/file/file/{0}'.format(fid))
            self.write(val)

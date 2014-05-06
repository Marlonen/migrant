#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    server area  action
    author comger@gmail.com
"""

from kpages import url,mongo_conv
from kpages.model import ModelMaster
from utility import ActionHandler
from logic.pinying import get_pinyin


MArea = ModelMaster()('AreaModel')


@url(r"/admin/area")
class ServiceArea(ActionHandler):
    def get(self):
        pass


@url(r'/admin/area/list')
class ServerAreaList(ActionHandler):
    def get(self):
        page = int(self.get_argument('page',0))
        lst = MArea.page(page=page)
        self.render('admin/arealist.html',data=lst)

@url(r"/admin/area/save")
class ServerAreaSave(ActionHandler):
    def post(self):
        try:
            obj = MArea.fetch_data(self)
            if 'listname' not in obj:
                obj['listname'] = get_pinyin(obj['name'])
            
            obj['_id'] = self.get_argument('_id',None)

            r = MArea.save(obj) 
            self.write(dict(status=True, data = r))
        except Exception as e:
            print e
            self.write(dict(status=False, errmsg = e.message))

    def get(self):
        _id = self.get_argument("id", None)
        info = {}
        if _id:info = MArea.info(_id)
        self.render('admin/areainfo.html', info=info)

@url(r"/admin/area/delete")
class ServerAreaDelete(ActionHandler):
    def post(self):
        _id = self.get_argument("id", None)
        pass






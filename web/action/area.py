# -*- coding:utf-8 -*- 
#!/usr/bin/env python
"""
    author comger@gmail.com
"""

from kpages import url
from kpages.model import ModelMaster
from utility import BaseHandler


areamodel = ModelMaster()('AreaModel')

@url(r'/area')
class Area(BaseHandler):
    def get(self):
        user = ModelMaster()('AccountModel').info(self.uid)
        area_id = user.get('area',None)
        if not area_id:
            self.redirect('/profile')

        areainfo = areamodel.info(area_id)

        self.render('action/area.html',areainfo=areainfo)

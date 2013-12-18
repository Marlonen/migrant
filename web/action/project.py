# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    migrant 前端展示公共页面
"""
import datetime
import re
from kpages import url
from utility import BaseHandler
from logic.project import ProjectModel,TName as TProject
from logic.category import TName as T_Category
from logic.account import TName as T_Account
from logic.utility import m_page,m_info
from logic.label import add as addlabel,suggest

strip_tag_pat=re.compile('</?\w+[^>]*>')

@url(r'/project?')
class Project(BaseHandler):
    def get(self):
        r,projects = m_page(TProject)
        self.render('action/project.html',projects=projects)


@url(r'/project/info/(.*)')
class ProjectInfo(BaseHandler):
    def get(self,_id=None):
        r,v = m_info(TProject,_id)
        
        ur,uv = m_info(T_Account,v['author'])
        v['authorname'] = uv.get('nickname',None) or uv['username']

        self.render('action/projectinfo.html',info = v)

@url(r'/project/create')
class CreateProject(BaseHandler,ProjectModel):
    def post(self):
        try:
            addon = datetime.datetime.now()
            data = self._get_postdata(addon=addon)
            r,v = self._save(data)
            for i in data.get('labels',()):
                if i:
                    addlabel(3,i)

            self.write(dict(status=r,data=v)) 
        except Exception as e:
            self.write(dict(status=False,data=e.message))

    def get(self):
        r,self.categorys = m_page(T_Category,size=10)        
        self.render('action/projectsave.html')

@url(r'/project/label?')
class ProjectLabel(BaseHandler):
    def get(self):
        since = self.get_argument('since',None)
        keys = self.get_arguments('key')
        cond = {'labels':{'$in':keys}}
        r,project = m_page(TProject,since=since,**cond)
        for n in project:
            r,user = m_info(T_Account,n.get('author'))
            n['authorname'] = user.get('nickname',user.get('username'))

        self.labels = suggest(3)
        self.render('action/projectlist.html',project=project,since=since, title=keys)


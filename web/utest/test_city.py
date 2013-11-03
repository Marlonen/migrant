# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
"""
import json
from kpages import LogicContext,reflesh_config
from logic.city import add
from logic.utility import m_page,m_update
from unittest import TestCase

class CityCate(object):
    _url = 'http://d.360buy.com/area/get?fid={0}'
    def test_add(self):
        ps= self.get_citys()
        for p in ps:
            if p['id']<100:
                print p['name'],p['id']
                r,v=add(p['name'])
                cs = self.get_citys(p['id'])
                for c in cs:
                    print '**',c['name']
                    rr,vv = add(c['name'],v['_id'],1)
                    xs = self.get_citys(c['id'])
                    for x in xs:
                        print '****',x['name']
                        rrr,vvv = add(x['name'],vv['_id'],2)
    
    def get_citys(self,fid=0):
        url = self._url.format(fid)
        doc = pyq(url=url)
        text = doc.text()[21:-1]
        try:
            return json.loads(text)
        except:
            print text
            return []


class DemoCase(TestCase):
    def setUp(self):
        pass

    def test_upadte(self):
        r,parents =  m_page('city',size = 1000, parent=None)
        for i,item in enumerate(parents):
            m_update('city',item.get('_id'),id=i)
            r,rs = m_page('city',size=1000,parent=item.get('_id'))
            for n,city in enumerate(rs):
                m_update('city',city.get('_id'),id=int(str(i)+str(n)))
                r,items = m_page('city',size=1000,parent=city.get('_id'))
                for m,_city in enumerate(items):
                    m_update('city',_city.get('_id'),id=int(str(i)+str(n)+str(m)))


        print 'update end'
        parents =  m_page('city',level=0,parent=None)
        print parents
        

if __name__ == '__main__':
    from pyquery import PyQuery as pyq
    case = CityCate()
    reflesh_config('setting.py')
    with LogicContext():
        case.test_add()


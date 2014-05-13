# -*- coding:utf-8 -*- 
"""
    account logic (curd)
    author comger@gmail.com
"""
from kpages import not_empty,get_context,mongo_conv
from kpages.model import *
#from utility import m_update,m_del,m_page,m_exists,m_info,BaseModel
from utils.email_utils import send_mail, get_email_content
from utils.string_utils import random_key,hashPassword

TName = 'account'
Tb = lambda :get_context().get_mongo()[TName]

INIT, ACTIVATED, IDENTIFIED = range(3)


class AccountModel(Model):
    _name = TName
    _fields = dict(
        username = CharField(required=True),
        password = CharField(required=True),
        city = CharField(),
        mobile = CharField(),
        isadmin = FloatField(initial=False)
    )

    def add(self, username, password, city=None, **kwargs):
        try:
            not_empty(username, password)
            r = self.exists(username=username)
            if not r:
                val = dict(username=username, password=hashPassword(password), city=city)
                _id = self.insert(val,**kwargs)
                val['_id'] = str(_id)
                return True, val
            else:
                return False, 'EXISTS'
        except ValueError:
            return False, 'NO_EMPTY'


    def reset_pwd(self, uid, old_password, new_password):
        try:
            not_empty(uid, old_password, new_password)
            _id = ObjectId(uid)
            kwargs = dict(_id=_id, password=hashPassword(old_password))
            valid = self.exists(**kwargs)
            if valid:
                self.update(uid, password= hashPassword(new_password))
                return True, 'OK'
            else:
                return False, 'INVALIDED'
        except ValueError:
            return False, 'NO_EMPTY'


    def apply_active_account(self, username, host):
        try:
            not_empty(username)
            existed =self.exists(username=username)
            if existed:
                key = random_key()
                redis = get_context().get_redis()
                redis.set(key, username, 60 * 60)
                r = send_mail([username], '账号激活',
                              get_email_content('email_active_account.html',
                                  host=host, key=key, username=username))
                return r, 'OK' if r else 'FAIL'
            else:
                return False, 'NO_EXIST'
        except ValueError:
            return False, 'NO_EMPTY'


    def active_account(self,key):
        try:
            not_empty(key)
            redis = get_context().get_redis()
            username = redis.get(key)
            if not username:
                return False, 'EXPIRED'
            existed = self.exists(username=username)
            if existed:
                self.update(username,key='username',status=ACTIVATED)
                return True, dict(username=username)
            else:
                return False, 'NO_EXIST'
        except ValueError:
            return False, 'NO_EMPTY'


    def forgot_pwd(self,username,host):
        try:
            not_empty(username)
            existed = self.exists(username=username)
            if existed:
                key = random_key()
                redis = get_context().get_redis()
                redis.set(key, username, 60 * 60)
                r = send_mail([username], '找回密码',
                              get_email_content('email_forget_password.html',
                                  host=host, key=key, username=username))
                return r, 'OK' if r else 'FAIL'
            else:
                return False, 'NO_EXIST'
        except ValueError:
            return False, 'NO_EMPTY'


    def reset_forgotten_password(self, key, new_password):
        try:
            not_empty(key, new_password)
            redis = get_context().get_redis()
            username = redis.get(key)
            if not username:
                return False, 'EXPIRED'

            existed = self.exists(username=username)
            if existed:
                self.update(username,key='username', password=hashPassword(new_password))
                return True, 'OK'
            else:
                return False, 'NO_EXIST'

        except ValueError:
            return False, 'NO_EMPTY'


    def login(self, username, password, isadmin=None):
        try:
            not_empty(username, password)
            cond = dict(username=username, password=hashPassword(password))
            #cond = dict(username=username, password=password)
            if isadmin:
                cond.update(isadmin=isadmin)

            r = self.exists(**cond)
            if r:
                r = mongo_conv(r)
                return True, r
            else:
                return False, 'NO_EXISTED'
        except ValueError:
            return False, 'NO_EMPTY'
        except Exception as e:
            return False, e.message


    def auth_login(self, site,otherid,name,**kwargs):
        try:
            not_empty(site,otherid,name)
            r = self.exists(site=site,otherid=otherid,name=name)
            if r:
                r = mongo_conv(r)
                return True,r
            else:
                val = dict(site=site,otherid=otherid,name=name)
                _id = self.insert(val)
                val['_id'] = str(_id)
                return True,val
        except Exception as e:
            return False,e.message



    def conv_user(obj):
        if isinstance(obj, (list, tuple)):
            for d in obj:
                conv_user(d)

        elif isinstance(obj,dict):
            r,v = self.info(obj['uid'])
            if r:
                obj['username'] = v['username']
            else:
                obj['username'] = 'deleted user'

#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    文件管理
"""
from PIL import Image
from cStringIO import StringIO
from tornado import gen
from bson import ObjectId
from kpages import not_empty,get_context,mongo_conv
from asyncgridfs import GridFS

IMG_GFS = 'images'
THUMBNAIL_GFS = 'thumbnails'
FILE_GFS = 'files'


def _resize_image(content,fmt,size=__conf__.IMG_MAX_SIZE):
    img = Image.open(StringIO(content))
    w,h = img.size
    mw, mh = size
    if w > mw or h > mh:
        _rw, _rh = float(w) / mw, float(h) / mh
        r = max((_rw, _rh))
        _w, _h = int(w / r), int(h / r)
        im = img.resize((_w, _h), Image.ANTIALIAS)
        buf = StringIO()
        im.save(buf,fmt)
        content = buf.getvalue()
    
    return content


def get_file(fid, ftype, callback=None):
    db = get_context().get_asyncmongo()

    if ftype=='image':
        fs = GridFS(db, IMG_GFS)
    elif ftype=='thumbnail':
        fs = GridFS(db, THUMBNAIL_GFS)
    elif ftype=='file':
        fs = GridFS(db, FILE_GFS)
    
    fid = ObjectId(fid)
    fs.get(fid, callback=callback) 

def put_file(body, filename, **kwargs):
    db = get_context().get_asyncmongo()
    fs = GridFS(db, FILE_GFS)
    kwargs.update(filename=filename)
    fs.put(body,**kwargs)


@gen.coroutine
def put_image(body, filename, fmt,**kwargs):
    db = get_context().get_asyncmongo()
    kwargs.update(filename=filename)
    
    fs = GridFS(db, IMG_GFS)
    fid =yield gen.Task(fs.put,body,**kwargs)
    try:
        thumbnail = _resize_image(body,fmt,__conf__.THUMBNAIL_SIZE)
        
        tfs = GridFS(db, THUMBNAIL_GFS)
        tfid = yield gen.Task(tfs.put,thumbnail,_id=fid,**kwargs)
    except Exception as e:
        yield gen.Task(fs.delete,fid)
        print e
        raise

    raise gen.Return(fid)


@gen.coroutine
def del_image(fid):
    fid = ObjectId(fid)
    db = get_context().get_asyncmongo()
    tfs = GridFS(db,THUMBNAIL_GFS)
    yield gen.Task(tfs.delete,fid)
    
    fs = GridFS(db,IMG_GFS)
    yield gen.Task(fs.delete,fid)



def file_page(page,size=10,ftype='image', callback=None):
    db = get_context().get_asyncmongo()
    if ftype=='image':
        fs = GridFS(db,THUMBNAIL_GFS)
    elif ftype=='file':
        fs = GridFS(db,FILE_GFS)
    
    fs.find(skip=(page+1)*size,limit=size,callback=None)


import asyncmongo
@gen.coroutine
def image_page(page,size=10,ftype='image',callback=None):
    db = get_context().get_asyncmongo()
    tb = db[THUMBNAIL_GFS+'.files']
    
    lst,err = yield gen.Task(tb.find,skip=page*size,limit=size)
    cmd = dict(count=THUMBNAIL_GFS+'.files')
    rs,err = yield gen.Task(db.command,cmd)
    count = rs[0]['n']
    raise gen.Return((lst[0],count))

def conv(record, table=None):
    ts, fname = record['filename'].split('_', 1)
    ret = {
        "_id": str(record['_id']),
        "filename": fname,
        "datetime": record['uploadDate'].strftime("%Y-%m-%d %H:%M:%S"),
        "is_dir": False,
        "is_photo": table == "image",
        "filesize": record.get('length',0),
        "contentType": record['contentType'],
        "url": "/file/{table}/{fid}".format(table=table, fid=str(record['_id'])),
    }
    if ret['is_photo']:
        ret['thumbnail'] = "/file/thumbnail/{fid}".format(
            fid=str(record['_id']))
    return ret

"""
This is the global configuration of web app

@author cmaj135@gmail.com
@version 1.0 2013-11-11
"""
DEBUG = True
DB_NAME = 'migrant'
DB_HOST = 'localhost'
PORT = 8888
CACHE_HOST = 'localhost'
ACTION_DIR = ('action', 'restful', 'admin')

IMG_MAX_SIZE = (1600,1600)
THUMBNAIL_SIZE = (200,200)
#the email smpt configuration
SMTP_FROM = 'migrant_service@126.com'
SMTP_HOST = 'smtp.126.com'
SMTP_PORT = 25
SMTP_USER = 'migrant_service@126.com'
SMTP_PASSWORD = 'migrant123'

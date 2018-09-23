# -*- coding: utf-8 -*-

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Secret'
    PORT = 3002
    HOST = '0.0.0.0'

 
class Development(Config):
    DEBUG = True
    ENV = 'Development'
    DB_USERNAME = "DB_USERNAME"
    DB_PASSWORD = "DB_PASSWORD"
    DB_DATABASE_NAME = "DB_DATABASE_NAME"
    DB_HOST = "DB_HOST"
    DB_PORT = "DB_PORT"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_HOST+':'+DB_PORT+'/'+DB_DATABASE_NAME


class Testing(Config):
    TESTING = True
    ENV = 'Testing'
    DB_USERNAME = "DB_USERNAME"
    DB_PASSWORD = "DB_PASSWORD"
    DB_DATABASE_NAME = "DB_DATABASE_NAME"
    DB_HOST = "DB_HOST"
    DB_PORT = "DB_PORT"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_HOST+':'+DB_PORT+'/'+DB_DATABASE_NAME

 
class Production(Config):
    pass    
 
config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
 
    'default': Development
}
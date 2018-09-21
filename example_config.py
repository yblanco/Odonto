# -*- coding: utf-8 -*-

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PORT = 3002
    HOST = '0.0.0.0'
 
class Development(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave'
    ENV = 'Development'

class Testing(Config):
    TESTING = True
    ENV = 'Testing'
 
class Production(Config):
    pass    
 
config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
 
    'default': Development
}
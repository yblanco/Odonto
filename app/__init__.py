# -*- coding: utf-8 -*-
from flask import Flask
from config import config
 
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
 
    # Configuracion de los BluePrints
    from .home import home as home
    app.register_blueprint(home)
 
    return app
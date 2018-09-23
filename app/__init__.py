# -*- coding: utf-8 -*-
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()
 
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    # Configuracion de los BluePrints
    from .home import home as home
    app.register_blueprint(home)
    from .auth import auth as auth
    app.register_blueprint(auth)
 
    return app
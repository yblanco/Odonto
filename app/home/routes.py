# -*- coding: utf-8 -*-
from . import home as home
from controller import homeController
from flask_login import login_required

controller = homeController()


@home.route('/')
def home_page():
	return controller.home()


@home.route('/index')
@login_required
def index():
	return controller.index()
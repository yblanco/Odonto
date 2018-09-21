# -*- coding: utf-8 -*-
from . import home as home
from controller import homeController


controller = homeController()


@home.route('/')
def home_page():
	return controller.home()

@home.route('/index')
def index():
	return controller.index()
# -*- coding: utf-8 -*-
from jinja2 import TemplateNotFound
from controller import homeController
from . import home as home


controller = homeController()
 
@home.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)

@home.route('/')
def home_page():
	return controller.home()

@home.route('/index')
def index():
	return controller.index()
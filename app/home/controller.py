# -*- coding: utf-8 -*-
from flask import request, render_template


class homeController(object):

    def home(self):
    	return render_template('welcome.html')

    def index(self):
    	return render_template('index.html')
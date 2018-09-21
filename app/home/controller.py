# -*- coding: utf-8 -*-
from flask import render_template


class homeController(object):

    def home(self):
    	return render_template('welcome.html')

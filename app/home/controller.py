# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
from flask_login import current_user


class homeController(object):

    def home(self):
    	if current_user.is_authenticated:
            return redirect(url_for('home.index'))
    	return render_template('welcome.html')

    def index(self):
        return render_template('index.html', title='Dashboard')

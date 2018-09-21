# -*- coding: utf-8 -*-
from flask import render_template, request
from flask_login import LoginManager, login_user, logout_user

#login_manager = LoginManager()


class authController(object):

    def login(self):
    	if request.method == 'POST':
    		username = request.form['username']
        	password = request.form['password']
        	if password == username:
        		login_user(user)
        		return redirect(request.args.get("next"))
        	else:
        		return abort(401)
    		
    	return render_template('login.html')
    	

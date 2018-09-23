# -*- coding: utf-8 -*-
from . import auth as auth
from controller import authController
from flask_login import login_required

controller = authController()

@auth.route('/', methods=['GET', 'POST'])
def login():
	return controller.login()

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
	return controller.logout()

@auth.route('/createAdmin', methods=['GET'])
def admin():
	return controller.generateAdmin()

@login_required

@auth.route('/profile', methods=['GET', 'POST'])
def profile():
	return controller.profile()
@auth.route('profileImg', methods=['POST'])
def image():
	return controller.image()

@auth.route('password', methods=['POST'])
def password():
	return controller.password()
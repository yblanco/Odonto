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


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	return controller.profile()

@auth.route('/profileImg', methods=['POST'])
@login_required
def image():
	return controller.image()

@auth.route('/password', methods=['POST'])
@login_required
def password():
	return controller.password()

@auth.route('/users', methods=['GET'])
@login_required
def users():
	return controller.users()

@auth.route('/user', methods=['GET','POST'])
@login_required
def user():
	return controller.user()

@auth.route('/user/<id_user>', methods=['GET','POST'])
@login_required
def user_edit(id_user):
	return controller.user_edit(id_user)

@auth.route('/user/<id_user>/<id>', methods=['GET'])
@login_required
def user_status(id_user, id):
	return controller.user_status(id_user, id)


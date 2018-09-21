# -*- coding: utf-8 -*-
from . import auth as auth
from controller import authController


controller = authController()

@auth.route('/', methods=['GET', 'POST'])
def login():
	return controller.login()
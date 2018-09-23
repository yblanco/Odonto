# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from app import login_manager
from .models import USERS
import os
import time


class authController(object):

    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('home.index'))

    	if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            isValid = USERS.isValidUser(username,password)
            if isValid is not False:
                login_user(isValid)
                return redirect(request.args.get("next")  or url_for('home.index'))
            else:
                flash('Credenciales inválidas', 'danger')
                return redirect(url_for('auth.login'))
    		
    	return render_template('login.html', ifadmin=USERS.existAdmin())

    def logout(self):
        logout_user()
        flash('Sesión Finalizada', 'info')
        return redirect(url_for('auth.login'))

    def profile(self):
        if request.method == 'POST':
            name = request.form.get('name')
            last_name = request.form.get('last_name')
            if current_user.updateUser(name, last_name, current_user.id_user):
                flash('Guardado', 'success')
            else:
                flash('Error al guardar', 'danger')
            return redirect(url_for('auth.profile'))
        return render_template('profile.html', title='Perfil de Usuario #'+current_user.id)

    def image(self):
            try:
                if request.method == 'POST':
                    if 'file' not in request.files:
                        flash('No existe Archivo Adjunto', 'warning')
                        raise Exception('File not found')

                    file = request.files['file']
                    if file.filename == '':
                        flash('No seleccionó ningún archivo', 'warning')
                        raise Exception('file not Selected')

                    if file:
                        allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
                        filename = str(current_user.id_user)+secure_filename(file.filename)
                        allowed_file = '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
                        if allowed_file:
                            try:
                                path = os.getcwd()+'/app/'+url_for('home.static', filename='img/users/')
                                filenewname = str(current_user.id)+"_"+str(str(time.time()).split('.')[0])+"."+filename.split('.')[-1]
                                file.save(os.path.join(path, filenewname))
                                if USERS.updateImg(filenewname, current_user.id_user):
                                    flash('Imagen subida', 'success')
                                else:
                                    flash('Imagen no guardada', 'warning')
                            except Exception as e:
                                flash('No se pudo subir la imagen', 'warning')
                                raise Exception(e)
                        else:
                            flash('Formato no permitido', 'warning')
                            raise Exception('File not allowed')
                    else:
                        flash('Error al Procesar Archivo', 'warning')
                        raise Exception('File has not value')

                else:
                    flash('Error de Ruta', 'danger')
            except Exception as e:
                print 'ERROR auth.controller.image: ', e
            finally:
                return redirect(url_for('auth.profile'))

    def password(self):
        if request.method == 'POST':
            password = request.form.get('password')
            newpassword = request.form.get('newpassword')
            newpasswordconfirm = request.form.get('newpasswordconfirm')
            if newpasswordconfirm == newpassword:
                if newpassword != password:
                    if USERS.verifyPassword(password, current_user.password):
                        if current_user.updatePassword(password, newpassword, current_user.id_user):
                            flash('Contraseña Guardada', 'success')
                        else:
                            flash('No se Pudo cambiar su contraseña', 'danger')
                    else:
                        flash('Contraseña inválida', 'danger')
                else:
                   flash('Contraseña igual a la actual', 'warning')
            else:
                flash('No coinciden las conraseñas', 'warning')
        else:
            flash('Error de Ruta', 'danger')
        return redirect(url_for('auth.profile'))

            


    def generateAdmin(self):
        if current_user.is_authenticated:
            return redirect(url_for('home.index'))

        return render_template('admin.html', result = USERS.createAdmin())
    	

@login_manager.user_loader
def load_user(user_id):
    return USERS.query.filter_by(id = user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    flash('Sesión no encontrada', 'warning')
    return redirect(url_for('home.home_page'))
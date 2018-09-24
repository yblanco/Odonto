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


    def generateAdmin(self):
        if current_user.is_authenticated:
            return redirect(url_for('home.index'))

        return render_template('admin.html', result = USERS.createAdmin())


    def logout(self):
        logout_user()
        flash('Sesión Finalizada', 'info')
        return redirect(url_for('auth.login'))

    def profile(self):
        if request.method == 'POST':
            name = request.form.get('name')
            last_name = request.form.get('last_name')
            if current_user.updateProfile(name, last_name, current_user.id_user):
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
                                filenewname = str(current_user.id)+"_"+USERS.randomString()+"."+filename.split('.')[-1]
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
                print 'ERROR auth.controller.image: ', str(e)
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

    def users(self):
        return render_template('users.html', title='Usuarios', users=USERS.users())

    def user(self):
        formdata = dict()
        if request.method == 'POST':
            try:
                formdata = request.form
                name = request.form.get('name')
                last_name = request.form.get('last_name')
                mail = request.form.get('mail')
                username = request.form.get('username')
                password = request.form.get('password')
                password_confirm = request.form.get('password_confirm')
                if password != '':
                    if password == password_confirm:
                        result = USERS.newUser(name, last_name, mail, username, password)
                        if result['result'] is True:
                            flash('Usuario guardado', 'success')
                            return  redirect(url_for('auth.user_edit', id_user= result['id_user']))
                        else:
                            flash(result['msg'], 'danger')
                    else:
                        flash('No coinciden las contraseñas', 'danger')
                else:
                    flash('Indique una contraseña', 'danger')

            except Exception as e:
                flash('Error al guardar el usuario', 'danger')
                print 'ERROR auth.controller.user: ', str(e)
        return render_template('user.html', title='Nuevo Usuario', form=formdata, edit=False, user = False)

    def user_edit(self,user_id):
        user = USERS.query.get(user_id)
        formdata = dict()
        if request.method == 'POST':
            try:
                formdata = request.form
                name = request.form.get('name')
                last_name = request.form.get('last_name')
                mail = request.form.get('mail')
                username = request.form.get('username')
                password = request.form.get('password')
                password_confirm = request.form.get('password_confirm')
                password_new = False
                if password_confirm != '' and  password != '':
                    password_new = password

                if password_new != False and password != password_confirm:
                    flash('Contraseñas no coinciden', 'danger')
                    raise Exception('Contraseñas no coinciden')
                else:
                    result = USERS.updateUser(user_id, name, last_name, password_new)
                    if result['result'] is True:
                        flash('Usuario actualizado', 'success')
                        return  redirect(url_for('auth.user_edit', id_user= user_id))
                    else:
                        flash(result['msg'], 'danger')

            except Exception as e:
                flash('Error al actualizar el usuario', 'danger')
                print 'ERROR auth.controller.user: ', str(e)

        return render_template('user.html', title='Editar Usuario '+user.username, user=user, form=formdata, edit=True)


    def user_status(self,id_user,id):
        if(USERS.updateStatus(id_user,id)):
            flash('Estatus Actualizado', 'success')
        else:
            flash('No se pudo Actualizar', 'danger')
        return redirect(url_for('auth.users'))

@login_manager.user_loader
def load_user(user_id):
    return USERS.query.filter_by(id = user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    flash('Sesión no encontrada', 'warning')
    return redirect(url_for('home.home_page'))
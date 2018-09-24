# -*- coding: utf-8 -*-
from app import db	
from sqlalchemy import func
from flask_login import UserMixin
import uuid
import random
import string
import bcrypt
import datetime


class STATUS(db.Model):
    __tablename__ = 'status'
    id_status = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(7), nullable=False, default='ENABLE')


class USERS(db.Model, UserMixin):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password =  db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(80), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id_status'), nullable=False)
    image = db.Column(db.String(255), nullable=False, default='default.png')
    registered_date = db.Column(db.DateTime, nullable=True)
    activated_date = db.Column(db.DateTime, nullable=True)
    modified_date = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(7), nullable=False, default='ENABLE')
    status_name = db.relationship('STATUS', backref='users', lazy=True)

    def __unicode__(self):
        return self.name[0]+'. '+self.last_name


    def __init__(self,name,last_name,mail,username, password):
        self.id = self.randomId()
        self.name = name
        self.last_name = last_name
        self.mail = mail
        self.username = username
        self.status_id = STATUS.query.filter_by(id=0).first().id_status
        self.password = self.hashPassword(password)
        self.registered_date = datetime.datetime.now()
        self.activated_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        self.last_login = datetime.datetime.now()
    
    @classmethod
    def randomId(self):
        while True:
            randomId = string.upper(''.join(random.choice(str(uuid.uuid4()).replace('-', '')) for _ in range(20)))
            if self.query.filter_by(id = randomId).count() == 0:
                break
    	return randomId

    @classmethod
    def randomString(self):
        return str(uuid.uuid4()).replace('-', '')

    @classmethod
    def hashPassword(self, password):
    	salt = bcrypt.gensalt()
    	return bcrypt.hashpw(password.encode('utf-8'), salt)

    @classmethod
    def verifyPassword(self, password, hashed):
    	return hashed.encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @classmethod
    def existAdmin(self):
        return self.query.filter_by(username='admin').count() > 0

    @classmethod
    def createAdmin(self):
        result = dict(
            result= False,
            msg= 'Usuario Ya existe'
        )
        if self.existAdmin() is not True:
            try:    
                password = self.randomString()
                newUser = self.newUser('Administrador', 'De Sistema', 'admin@admin', 'admin', password)
                if newUser['result']:
                    result['result'] = True
                    result['msg'] = 'Usuario creado correctamente'
                    result['username'] = add.username
                    result['password'] = password
                else:
                    result['msg'] = newUser['msg']
            except Exception as e:
                db.session.rollback()
                result['msg']  = str(e)
        return result

    @classmethod
    def isValidUser(self, username, password):
        result = False
        try:
            user = self.query.filter_by(username=username).first()
            if user is not None:
                if self.verifyPassword(password, user.password):
                    user.last_login = datetime.datetime.now()
                    db.session.commit()
                    result = user
        except Exception as e:
            db.session.rollback()
            print 'ERROR auth.models.isValidUser: ', username, '-', str(e)
        finally:
            return result

    @classmethod
    def updateProfile(self, name, last_name, id_user):
        result = False
        try:
            user = self.query.get(id_user)
            user.name = name
            user.last_name = last_name
            user.modified_date = datetime.datetime.now()
            db.session.commit()
            result = True
        except Exception as e:
            db.session.rollback()
            print 'ERROR auth.models.updateUser: ', name+' '+last_name, '-', str(e)
        finally:
            return result

    @classmethod
    def updateImg(self, filename, id_user):
        result = False
        try:
            user = self.query.get(id_user)
            user.image = filename
            user.modified_date = datetime.datetime.now()
            db.session.commit()
            result = True
        except Exception as e:
            db.session.rollback()
            print 'ERROR auth.models.updateUser: ', filename, '-', str(e)
        finally:
            return result

    @classmethod
    def updatePassword(self, password, newpassword, id_user):
        result = False
        try:
            user = self.query.get(id_user)
            if self.verifyPassword(password, user.password):
                user.password = self.hashPassword(newpassword)
                user.modified_date = datetime.datetime.now()
                db.session.commit()
                result = True
        except Exception as e:
            db.session.rollback()
            print 'ERROR auth.models.updatePassword: ', id_user, '-', str(e)
        finally:
            return result

    @classmethod
    def users(self):
        result = False
        try:
            result = self.query.filter_by(status = 'ENABLE').all()
        except Exception as e:
            print 'ERROR auth.models.users: '+str(e)
        finally:
            return result

    @classmethod
    def newUser(self, name, last_name, mail, username, password):
        result = dict(
            result=False,
            msg='Error guardando el Usuario')
        try:
            check = USERS.query.filter((USERS.username == username) | (USERS.mail == mail)).count()
            if check == 0:
                new = USERS(name, last_name, mail, username, password)
                db.session.add(new)
                db.session.commit()
                result['id_user'] = new.id_user
                result['result'] = True
                result['msg'] = 'Success'
            else:
                result['msg'] = 'Username o Email duplicado'
        except Exception as e:
            db.session.rollback()
            print 'ERROR auth.models.newUser: '+'[name:'+name+'|'+'last_name:'+last_name+'|'+'mail:'+mail+'|'+'username:'+username+']-'+str(e)
        finally:
            return result
    @classmethod
    def updateUser(self, id_user, name, last_name, password):
        result = dict(
            result=False,
            msg='Error actualizando el Usuario')
        try:
            user = self.query.get(id_user)
            user.name= name
            user.last_name = last_name
            if password != False:
                user.password = self.hashPassword(password)
            db.session.commit()
            result['result'] = True
            result['msg'] = 'Success'
        except Exception as e:
            db.session.rollback()
            print 'ERROR auth.models.newUser: '+'[name:'+name+'|'+'last_name:'+last_name+'|'+'id_user:'+id_user+']-'+str(e)
        finally:
            return result

    @classmethod
    def updateStatus(self, id_user, id):
        result = False
        try:
            user = self.query.get(id_user)
            user.modified_date = datetime.datetime.now()
            user.status_id = STATUS.query.filter_by(id=id).first().id_status
            db.session.commit()
            result = True
        except Exception as e:
            db.session.rollback()
            print 'ERROR auth.models.updateStatus: '+id_user+'_'+status_id+'-'+str(e)
        finally:
            return result
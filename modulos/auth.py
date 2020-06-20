import os
import sys

from .db import (
    Usuario
) 


def agregar_usuario(request, session):
    data = {
        "tabla" : "Usuario",
        "accion": "alta",
        "resultado": "NOOP",
        "mensaje": "No Procesado"
    }
    email = request.form.get('email')
    password = request.form.get('password')
    if check_usuario(email, session):
        data['resultado'] = 'KO'
        data['mensaje'] = 'El usuario %s ya existe!' % (email)
        data['email'] = email
        return data
    else:
        try:
            u = Usuario(email=email)
            u.set_password(password)
            session.add(u)
            session.commit()
            data['resultado'] = 'OK'
            data['mensaje'] = 'Usuario %d: %s creado' % (u.id, email)
            data['email'] = email
        except Exception as e:
            data['resultado'] = 'KO'
            data['mensaje'] = str(e)
        finally:
            session.close()
            return data

def check_usuario(email, session):
    try:
        u = session.query(Usuario).filter_by(email=email).first()
        if u is None:
            return False
        else:
            return True
    except Exception as e:
        print(__name__, "Error chequeando usuario: %s[%s]" % (email, str(e)))
        return True

def traer_usuario(email, session):
    try:
        u = session.query(Usuario).filter_by(email=email).first()
        return u
    except Exception as e:
        print(__name__, "Error trayendo usuario: %s[%s]" % (email, str(e)))
        return None

def buscar_usario(request, session):
    email = request.form.get('email')
    password = request.form.get('password')

    data = {
        "tabla" : "Usuario",
        "accion": "ingreso",
        "resultado": "NOOP",
        "mensaje": "No Procesado",
        "email" : email
    }

    u = traer_usuario(email, session)

    if u is None:
        data['resultado'] = 'KO'
        data['mensaje'] = '%s: No existe el usuario'
        data['email'] = None
        return data
    if not u.check_password(password):
        data['resultado'] = 'KO'
        data['mensaje'] = 'Password incorrecta'
        data['email'] = email
        return data
    session.close()
    data['resultado'] = 'OK'
    data['mensaje'] = 'Bienvendo %s!' % (email)
    return data

def reset_password(request, session):
    data = {
        "tabla" : "Usuario",
        "accion": "reset pass",
        "resultado": "NOOP",
        "mensaje": "No Procesado",
        "email" : None
    }

    email = request.form.get('email')
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')
    data['email'] = email
    u = traer_usuario(email, session)

    if u is None:
        data['resultado'] = 'KO'
        data['mensaje'] = 'Usuario incorrecto'
        return data
    if not u.check_password(oldpassword):
        data['resultado'] = 'KO'
        data['mensaje'] = 'Password original incorrecta'
        return data

    u.set_password(newpassword)
    session.commit()
    session.close()
    data['resultado'] = 'OK'
    data['mensaje'] = 'Password de %s modificada' % (email)
    return data

def borrar_usuario(request, session):
    data = {
        "tabla" : "Usuario",
        "accion": "Baja",
        "resultado": "NOOP",
        "mensaje": "No Procesado"
    }
    email = request.form.get('email')
    password = request.form.get('password')
    u = traer_usuario(email, session)
    if u is None:
        data['resultado'] = 'KO'
        data['mensaje'] = '%s: Usuario incorrecto' % (email)
        session.close()
        return data
    if not u.check_password(password):
        data['resultado'] = 'KO'
        data['mensaje'] = 'Password incorrecta'
        session.close()
        return data
        
    session.delete(u)
    session.commit()
    session.close()
    data['resultado'] = 'OK'
    data['mensaje'] = 'Usuario %s eliminado' % (email)
    return data
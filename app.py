from modulos.csv import CSV
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, render_template
import json

from model.db import (
    Base, 
    Persona, 
    Usuario, 
    Provincia, 
    Sector, 
    Ambito, 
    Localidad, 
    Escuela,
    DomicilioEscuela,
    TedNivEscuela,
    TipoNivelEducacion,
    TipoEducacion,
    NivelEducacion)

engine = create_engine('sqlite:///db/escuela.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        "titulo": "Inicio"
    }
    return render_template('inicio.html', data=data)

@app.route('/persona/<nombre>', methods=['GET','POST'])
def persona(nombre):
    session = DBSession()
    if request.method == 'POST':
        p = Persona(nombre=nombre)
        session.add(p)
        session.commit()
        return '<h1>%s creado  Ok</h1>'%(nombre)
    else:
        p = session.query(Persona).filter(Persona.nombre == nombre).first()
        if p is None:
            return '<h1>No existe la persona de nombre %s</h1>' % (nombre)
        else:
            return json.dumps(p.dict(), ensure_ascii=False)

@app.route('/personas')
def listar_personas():
    session = DBSession()
    persons = session.query(Persona).all()
    ret = [p._dict() for p in persons]
    return json.dumps(ret)


def listar_persona(id):
    session = DBSession()
    p = session.query(Persona).filter(Persona.id == id).all()
    for per in p:
        print(per.nombre)

@app.route('/registro', methods=['GET','POST'])
def agregar_usuario():
    data = {
        "titulo": "Alta",
        "tituloform": "Alta de Usuario"
    }
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        session = DBSession()
        u = Usuario(email=email)
        u.set_password(password)
        session.add(u)
        session.commit()
        return '<h1>Usuario %s registrado' % (email)
    elif request.method == 'GET':
        return render_template('registro.html', data=data)
    else:
        return render_template('nomethod.html')


@app.route('/ingreso', methods=['GET','POST'])
def buscar_usuario():
    data = {
        "titulo": "Ingreso",
        "tituloform" : "Ingreso al Sistema"
    }
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session = DBSession()
        u = session.query(Usuario).filter_by(email=email).first()
        if u is None:
            return '<h1>Usuario %s incorrecto' % (email)
        if not u.check_password(password):
            return '<h1>Usuario %s password incorrecta' % (email)
        data["titulo"] = "Menú"
        return render_template('menu.html', data=data)
    elif request.method == 'GET':
        return render_template('ingreso.html', data=data)
    else:
        return render_template('nomethod.html')

@app.route('/reset', methods=['GET','POST'])
def reset_password():
    data = {
        "titulo": "Password",
        "tituloform": "Cambio de Password"
    }
    if request.method == 'POST':
        email = request.form.get('email')
        oldpassword = request.form.get('oldpassword')
        newpassword = request.form.get('newpassword')
        session = DBSession()
        u = session.query(Usuario).filter_by(email=email).first()
        if u is None:
            return '<h1>Usuario %s incorrecto' % (email)
        if not u.check_password(oldpassword):
            return '<h1>Usuario %s password original incorrecta' % (email)
        u.set_password(newpassword)
        session.commit()
        return '<h1>Password de %s actualizada' % (email)
    elif request.method == 'GET':
        return render_template('reset.html', data=data)
    else:
        return render_template('nomethod.html')

@app.route('/baja', methods=['GET','POST'])
def borrar_usuario():
    data = {
        "titulo": "Baja",
        "tituloform": "Baja de Usuario"
    }
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session = DBSession()
        u = session.query(Usuario).filter_by(email=email).first()
        if u is None:
            return '<h1>Usuario %s incorrecto' % (email)
        if not u.check_password(password):
            return '<h1>Usuario %s, password incorrecta' % (email)
        session.delete(u)
        session.commit()
        return '<h1>Usuario %s eliminado. A la bosta!' % (email)
    elif request.method == 'GET':
        return render_template('baja.html', data=data)
    else:
        return render_template('nomethod.html')

@app.route('/provincias')
def listar_provincias():
    session = DBSession()
    provs = session.query(Provincia).all()
    ret = [p._dict() for p in provs]
    data = {
        "titulo": "Provincias",
        "recs" : ret
    }
    return render_template('keyval.html', data=data)

@app.route('/sectores')
def listar_sectores():
    session = DBSession()
    secs = session.query(Sector).all()
    ret = [p._dict() for p in secs]
    data = {
        "titulo": "Sectores",
        "recs" : ret
    }
    return render_template('keyval.html', data=data)

@app.route('/ambitos')
def listar_ambitos():
    session = DBSession()
    ambs = session.query(Ambito).all()
    ret = [p._dict() for p in ambs]
    data = {
        "titulo": "Ambitos",
        "recs" : ret
    }
    return render_template('keyval.html', data=data)

@app.route('/localidades')
def localicades_provincia():
    session = DBSession()
    provs = session.query(Provincia).all()
    ret = [p._dict() for p in provs]
    data = {
        "titulo": "Localidades por Provincia",
        "recs" : ret,
        "url" : 'localidad'
    }
    return render_template('keyval.html', data=data)

@app.route('/localidad/<pciaid>')
def listar_localidades(pciaid):
    session = DBSession()
    pcia = session.query(Provincia).filter_by(id=pciaid).first()
    locs = session.query(Localidad).filter_by(provincia_id=pciaid).all()
    ret = [p._dict() for p in locs]
    data = {
        "titulo": "Escuelas por localidad: %s" % (pcia.nombre),
        "recs" : ret,
        "url" : 'escuelas'
    }
    return render_template('localidades.html', data=data)

@app.route('/escuela/<id>')
def escuela(id):
    session = DBSession()
    esc = session.query(Escuela).filter_by(id=id).first()
    domicilio = session.query(DomicilioEscuela).filter_by(escuela_id=id).first()
    niveles = session.query(TedNivEscuela).filter_by(escuela_id=id).all()
    newnes = []
    for n in niveles:
        tne = session.query(TipoNivelEducacion).filter_by(id=n.tipoNivelEducacion_id).first()
        te = session.query(TipoEducacion).filter_by(id=tne.tipoeducacion_id).first()
        ne = session.query(NivelEducacion).filter_by(id=tne.niveleducacion_id).first()
        newne = {
            "tipo" : te._dict()['nombre'],
            "nivel" : ne._dict()['nombre'].replace('_',' ')
        }
        newnes.append(newne)

    rec = esc._dict()
    rec['domicilio'] = domicilio
    rec['tne'] = newnes

    data = {
        "titulo": "Datos de Escuela",
        "rec" : rec,
        "url" : None
    }
    return render_template('escuela.html', data=data) 

@app.route('/escuelas/<locid>')
def escuelas(locid):
    session = DBSession()
    loc = session.query(Localidad).filter_by(id=locid).first()
    escs = session.query(Escuela).filter_by(localidad_id=locid).all()
    ret = [p._dict() for p in escs]
    #return json.dumps(ret, ensure_ascii=False)
    data = {
        "titulo": "Escuelas por localidad: %s, %s" % (loc.nombre.title(), loc.provincia.nombre),
        "recs" : ret,
        "url" : 'escuela'
    }
    return render_template('escuelas.html', data=data)    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
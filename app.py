from modulos.csv import CSV
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, request, render_template, flash
import json
import modulos.auth as auth

from model.db import (
    Base, 
    Provincia, 
    Sector, 
    Ambito, 
    Localidad, 
    Escuela,
    DomicilioEscuela,
    TedNivEscuela,
    TipoNivelEducacion,
    TipoEducacion,
    NivelEducacion
)

engine = create_engine('sqlite:///db/escuela.db')
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# -----------------------------------------------------------
# Inicio
# -----------------------------------------------------------
@app.route('/')
def index():
    data = {
        "titulo": "Inicio"
    }
    return render_template('inicio.html', data=data)

# -----------------------------------------------------------
# Registro
# -----------------------------------------------------------
@app.route('/registro', methods=['GET','POST'])
def agregar_usuario():
    data = {
        "titulo": "Alta",
        "tituloform": "Alta de Usuario",
        "email": None
    }
    if request.method == 'POST':
        result = auth.agregar_usuario(request, DBSession())
        data = {
            "titulo": "Ingreso",
            "tituloform" : "Ingreso al Sistema",
            "email": result['email']
        }
        if result['resultado'] == 'OK':
            return render_template('ingreso.html', data=data)
        else:
            flash(result['mensaje'])
            return render_template('registro.html', data=data)
    elif request.method == 'GET':
        return render_template('registro.html', data=data)

# -----------------------------------------------------------
# Ingreso
# -----------------------------------------------------------
@app.route('/ingreso', methods=['GET','POST'])
def buscar_usuario():
    data = {
        "titulo": "Ingreso",
        "tituloform" : "Ingreso al Sistema",
        "email" : None
    }
    if request.method == 'POST':
        result = auth.buscar_usario(request,DBSession())
        if result['resultado'] == 'OK':
            session = DBSession()
            data = {
                "titulo": "Buscar escuela",
                "recs" : {
                        "provs" : session.query(Provincia).all(),
                        "ambs" : session.query(Ambito).all(),
                        "secs" : session.query(Sector).all()
                    },
                "url" : None,
                "email" : result['email']
            }    
            session.close()  
            return render_template('buscar.html', data=data)
        else:
            data['email'] = result['email']
            flash(result['mensaje'])
            return render_template('ingreso.html', data=data)
    elif request.method == 'GET':
        return render_template('ingreso.html', data=data)


# -----------------------------------------------------------
# Reset Password
# -----------------------------------------------------------
@app.route('/reset', methods=['GET','POST'])
def reset_password():
    data = {
        "titulo": "Password",
        "tituloform": "Cambio de Password",
        "email": None
    }
    if request.method == 'POST':
        result = auth.reset_password(request, DBSession())
        if result['resultado'] == 'OK':
            data = {
                "titulo": "Ingreso",
                "tituloform" : "Ingreso al Sistema",
                "email": result['email']
            }
            return render_template('ingreso.html', data=data)
        else:
            data['email'] = result['email']
            data['resultado'] = result['resultado']
            data['mensaje'] = result['mensaje']
            print(data)
            flash(result['mensaje'])
            return render_template('reset.html', data=data)
    elif request.method == 'GET':
        return render_template('reset.html', data=data)

# -----------------------------------------------------------
# Baja 
# -----------------------------------------------------------
@app.route('/baja', methods=['GET','POST'])
def borrar_usuario():
    data = {
        "titulo": "Baja",
        "tituloform": "Baja de Usuario"
    }
    if request.method == 'POST':
        result = auth.borrar_usuario(request, DBSession())
        data = {
            "titulo": "Inicio"
        }
        return render_template('inicio.html', data=data)        
    elif request.method == 'GET':
        return render_template('baja.html', data=data)

# -----------------------------------------------------------
# Buscar escuelas
# -----------------------------------------------------------
@app.route('/buscar')
def show():
    session = DBSession()
    data = {
        "titulo": "Buscar escuela",
        "recs" : {
                "provs" : session.query(Provincia).all(),
                "ambs" : session.query(Ambito).all(),
                "secs" : session.query(Sector).all()
            },
        "url" : None
    }
    return render_template('buscar.html', data=data)             

# -----------------------------------------------------------
# Escuelas seleccionadas
# -----------------------------------------------------------
@app.route('/escuelas/<int:pciaid>/<int:locid>/<int:secid>/<int:ambid>')
def escuelas(pciaid, locid, secid, ambid):
    print('escuelas',pciaid, locid, secid, ambid)
    session = DBSession()
    prov = session.query(Provincia).filter_by(id=pciaid).first()
    nombreloc = ""
    if locid == 0:
        print("locid es 0",locid)
        #sql = session.query(Escuela).join(Localidad).filter(Localidad.provincia_id==locid)
        escs = session.query(Escuela).join(Localidad).filter(Localidad.provincia_id==locid).all()
        nombreloc = "Todas las localidades"
    else:
        loc = session.query(Localidad).filter_by(id=locid).first()
        nombreloc = loc.nombre
        if secid == 0 and ambid == 0:   
            escs = session.query(Escuela).filter_by(localidad_id=locid).all()
        elif secid != 0 and ambid == 0:
            escs = session.query(Escuela)\
                .filter_by(localidad_id=locid, sector_id=secid).all()
        elif secid == 0 and ambid != 0:
            escs = session.query(Escuela)\
                .filter_by(localidad_id=locid, ambito_id=ambid).all()
        elif secid != 0 and ambid != 0:
            escs = session.query(Escuela)\
                .filter_by(localidad_id=locid, \
                    sector_id=secid, ambito_id=ambid).all()

    ret = [p._dict() for p in escs]
    session.close()
    data = {
        "titulo": "Escuelas por localidad: %s, %s" % (nombreloc.title(), prov.nombre.title()),
        "recs" : ret,
        "url" : 'escuela'
    }
    return render_template('escuelas.html', data=data)    

# -----------------------------------------------------------
# Datos de una escuela
# -----------------------------------------------------------
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

    session.close()

    data = {
        "titulo": "Datos de Escuela",
        "rec" : rec,
        "url" : None
    }
    return render_template('escuela.html', data=data) 

# -----------------------------------------------------------
# Localidades por provincia
# -----------------------------------------------------------
@app.route('/localidad/<pciaid>')
def listar_localidades(pciaid):
    session = DBSession()
    locs = session.query(Localidad).filter_by(provincia_id=pciaid).order_by(Localidad.nombre).all()
    ret = [p._dict() for p in locs]
    data = {
        "recs" : ret,
    }
    session.close()
    return json.dumps(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
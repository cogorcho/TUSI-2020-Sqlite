from modulos.csv import CSV
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, request, render_template
import json
import modulos.auth as auth
import modulos.datos as datos

from model.db import (
    Base, 
    Persona, 
    #Usuario, 
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
DBSession = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        "titulo": "Inicio"
    }
    return render_template('inicio.html', data=data)

@app.route('/registro', methods=['GET','POST'])
def agregar_usuario():
    data = {
        "titulo": "Alta",
        "tituloform": "Alta de Usuario"
    }
    if request.method == 'POST':
        result = auth.agregar_usuario(request, DBSession())
        return json.dumps(result)
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
        result = auth.buscar_usario(request,DBSession())
        if result['resultado'] == 'OK':
            data["titulo"] = "Menú"
            return render_template('menu.html', data=data)
        else:
            return json.dumps(result)
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
        result = auth.reset_password(request, DBSession())
        return json.dumps(result)
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
        result = auth.borrar_usuario(request, DBSession())
        return json.dumps(result)
    elif request.method == 'GET':
        return render_template('baja.html', data=data)
    else:
        return render_template('nomethod.html')

@app.route('/provincias')
def provincias():
    #session = DBSession()
    #provs = session.query(Provincia).all()
    #ret = [p._dict() for p in provs]
    data = {
        "titulo": "Provincias",
        "recs" : datos.provincias(DBSession())
    }
    return render_template('keyval.html', data=data)

@app.route('/sectores')
def sectores():
    data = {
        "titulo": "Sectores",
        "recs" : datos.sectores(DBSession())
    }
    return render_template('keyval.html', data=data)

@app.route('/ambitos')
def ambitos():
    data = {
        "titulo": "Ambitos",
        "recs" : datos.ambitos(DBSession())
    }
    return render_template('keyval.html', data=data)


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

@app.route('/localidades')
def localidades_provincia():
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
    locs = session.query(Localidad).filter_by(provincia_id=pciaid).order_by(Localidad.nombre).all()
    ret = [p._dict() for p in locs]
    data = {
        "recs" : ret,
    }
    return json.dumps(data)

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
        for e in escs:
            print(e)
        nombreloc = "Todas las localidades"
    else:
        loc = session.query(Localidad).filter_by(id=locid).first()
        print(locid,loc)
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
    data = {
        "titulo": "Escuelas por localidad: %s, %s" % (nombreloc.title(), prov.nombre.title()),
        "recs" : ret,
        "url" : 'escuela'
    }
    return render_template('escuelas.html', data=data)    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
from modulos.csv import CSV
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, request
import json

from model.db import Base, Persona, Usuario, Provincia, Sector, Ambito, Localidad, Escuela

engine = create_engine('sqlite:///db/escuela.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Ok</h1>'


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
            return json.dumps(p.json(), ensure_ascii=False)

@app.route('/personas')
def listar_personas():
    session = DBSession()
    persons = session.query(Persona).all()
    ret = [p.json() for p in persons]
    return json.dumps(ret)

def listar_persona(id):
    session = DBSession()
    p = session.query(Persona).filter(Persona.id == id).all()
    for per in p:
        print(per.nombre)

def agregar_usuario(email, passwd):
    session = DBSession()
    u = Usuario(email=email)
    u.set_password(passwd)
    session.add(u)
    session.commit()

def buscar_usuario(email, passwd):
    session = DBSession()
    u = session.query(Usuario).filter_by(email=email).first()
    print(u.nombre, u. passwd)

def reset_password(email, newpass):
    session = DBSession()
    u = session.query(Usuario).filter_by(email=email).first()
    u.set_password(newpasswd)

def borrar_usuario(email):
    session = DBSession()
    u = session.query(Usuario).filter_by(email=email).first()
    session.delete(u)
    session.commit

@app.route('/provincias')
def listar_provincias():
    session = DBSession()
    provs = session.query(Provincia).all()
    ret = [p.json() for p in provs]
    return json.dumps(ret, ensure_ascii=False)

@app.route('/sectores')
def listar_sectores():
    session = DBSession()
    secs = session.query(Sector).all()
    ret = [p.json() for p in secs]
    return json.dumps(ret, ensure_ascii=False)

@app.route('/ambitos')
def listar_ambitos():
    session = DBSession()
    ambs = session.query(Ambito).all()
    ret = [p.json() for p in ambs]
    return json.dumps(ret, ensure_ascii=False)

@app.route('/localidades/<pciaid>')
def listar_localidades(pciaid):
    session = DBSession()
    locs = session.query(Localidad).filter_by(provincia_id=pciaid).all()
    ret = [p.json() for p in locs]
    return json.dumps(ret, ensure_ascii=False)

@app.route('/escuela/<id>')
def escuela(id):
    session = DBSession()
    escs = session.query(Escuela).filter_by(id=id).all()
    ret = [p.json() for p in escs]
    return json.dumps(ret, ensure_ascii=False)

@app.route('/escuelas/<locid>')
def escuelas(locid):
    session = DBSession()
    escs = session.query(Escuela).filter_by(localidad_id=locid).all()
    ret = [p.json() for p in escs]
    return json.dumps(ret, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
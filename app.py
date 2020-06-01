from modulos.csv import CSV
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from model.db import Base, Persona, Usuario, Provincia, Sector, Ambito, Localidad

#engine = create_engine('sqlite:///db/gente.db')
engine = create_engine('sqlite:///db/escuela.db')


# Bind the engine to the metadat of the BAse class so that
# declaratives can be accessed through DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the DB
# and represents a staging zone for all objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the DB until you call the
# session.commit(). If you are not happy about the changes you
# can revert all of them back to last commit by calling
# session.rollback()
session = DBSession()

def agregar_persona(nombre):
    p = Persona(nombre=nombre)
    session.add(p)
    session.commit()

def listar_personas():
    persons = session.query(Persona).all()
    for person in persons:
        print(person.id, person.nombre)

def listar_persona(id):
    p = session.query(Persona).filter(Persona.id == id).all()
    for per in p:
        print(per.nombre)

def agregar_usuario(email, passwd):
    u = Usuario(email=email)
    u.set_password(passwd)
    session.add(u)
    session.commit()

def buscar_usuario(email, passwd):
    u = session.query(Usuario).filter_by(email=email).first()
    print(u.nombre, u. passwd)

def reset_password(email, newpass):
    u = session.query(Usuario).filter_by(email=email).first()
    u.set_password(newpasswd)

def borrar_usuario(email):
    u = session.query(Usuario).filter_by(email=email).first()
    session.delete(u)
    session.commit

def listar_provincias():
    provs = session.query(Provincia).all()
    for p in provs:
        print(p.id, p.nombre)

def listar_sectores():
    secs = session.query(Sector).all()
    for s in secs:
        print(s.id, s.nombre)

def listar_ambitos():
    ambs = session.query(Ambito).all()
    for a in ambs:
        print(a.id, a.nombre)

def listar_localidades(pciaid):
    locs = session.query(Localidad).filter_by(provincia_id=pciaid).all()
    for loc in locs:
        print(loc.id, loc.nombre.title())

if __name__ == '__main__':
    listar_provincias()
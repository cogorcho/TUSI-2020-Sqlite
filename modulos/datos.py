from .db import (
#    Persona, 
#    Usuario, 
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

def provincias(session):
    provs = session.query(Provincia).all()
    ret = [p._dict() for p in provs]
    return ret

def sectores(session):
    secs = session.query(Sector).all()
    ret = [p._dict() for p in secs]
    return ret

def ambitos(session):
    secs = session.query(Ambito).all()
    ret = [p._dict() for p in secs]
    return ret

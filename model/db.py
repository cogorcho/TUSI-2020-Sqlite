import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class Persona(Base):
    __tablename__ = 'Persona'
    # Columnas de la tabla Persona
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class Domicilio(Base):
    __tablename__ = 'Domicilio'
     # Columnas de la tabla Domicilio
    id = Column(Integer, primary_key=True)
    calle = Column(String(255), nullable=False)
    numero = Column(String(255), nullable=False)
    codpos = Column(String(255), nullable=False)
    calle = Column(String(255), nullable=False)
    persona_id = Column(Integer, ForeignKey('Persona.id'))
    persona = relationship(Persona)

class Ambito(Base):
    __tablename__ = 'Ambito'
    # Columnas de la tabla Ambito
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class Sector(Base):
    __tablename__ = 'Sector'
    # Columnas de la tabla Sector
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class Provincia(Base):
    __tablename__ = 'Provincia'
    # Columnas de la tabla Provincia
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class Localidad(Base):
    __tablename__ = 'Localidad'
    # Columnas de la tabla Localidad
    id = Column(Integer, primary_key=True)  
    nombre = Column(String(255), nullable=False)
    codigo = Column(String(32), nullable=False) 
    provincia_id = Column(Integer, ForeignKey('Provincia.id'))
    provincia = relationship(Provincia)

class Escuela(Base):
    __tablename__ = 'Escuela'
    #Columnas de la tabla Escuela
    id = Column(Integer, primary_key=True)  
    nombre = Column(String(255), nullable=False)
    codigo = Column(String(32), nullable=False) 
    sector_id = Column(Integer, ForeignKey('Sector.id'))
    ambito_id = Column(Integer, ForeignKey('Ambito.id'))
    localidad_id = Column(Integer, ForeignKey('Localidad.id'))
    sector = relationship(Sector)
    ambito = relationship(Ambito)
    localidad = relationship(Localidad)

class DomicilioEscuela(Base):
    __tablename__ = 'DomicilioEscuela'
     # Columnas de la tabla Domicilio
    id = Column(Integer, primary_key=True)
    calle = Column(String(255), nullable=False)
    numero = Column(String(255), nullable=False)
    codpos = Column(String(255), nullable=False)
    calle = Column(String(255), nullable=False)
    escuela_id = Column(Integer, ForeignKey('Escuela.id'))
    escuela = relationship(Escuela)

class TipoEducacion(Base):
    __tablename__ = 'TipoEducacion'
    # Columnas de la tabla TipoEducacion
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class NivelEducacion(Base):
    __tablename__ = 'NivelEducacion'
    # Columnas de la tabla NivelEducacion
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class TipoNivelEducacion(Base):
    __tablename__ = 'TipoNivelEducacion'
    # Columnas de la tabla TipoNivelEducacion
    id = Column(Integer, primary_key=True) 
    tipoeducacion_id = Column(Integer, ForeignKey('TipoEducacion.id'))
    niveleducacion_id = Column(Integer, ForeignKey('NivelEducacion.id'))
    TipoEducacion = relationship(TipoEducacion)
    NivelEducacion = relationship(NivelEducacion)

class TedNivEscuela(Base):
    __tablename__ = 'TedNivEscuela'
    # Columnas de la tabla TedNivEscuela
    id = Column(Integer, primary_key=True)
    escuela_id = Column(Integer, ForeignKey('Escuela.id'))
    tipoNivelEducacion_id = Column(Integer, ForeignKey('TipoNivelEducacion.id'))  
    escuela = relationship(Escuela) 
    tiponiveltducacion = relationship(TipoNivelEducacion) 

class Usuario(Base):
    __tablename__ = 'Usuario'
    id = Column(Integer, primary_key=True)
    email = Column(String(128), index=True, unique=True)
    password_hash = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# crear el engine para guardar los datos. La BD sqlite es un archivo
# gente.db
engine = create_engine('sqlite:///db/escuela.db')

# Crear todas las tablas en la engine.
# Equivale a Create Table en sql
Base.metadata.create_all(engine)

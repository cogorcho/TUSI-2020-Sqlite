# TUSI 2020.

## Demos básicas de:
### Registro de usuarios
### Ingreso al sistema
### Cambio de clave
### Baja del sistema

## A completar
### Manejo de sesion
### Reconfirmacion en la baja
### Listados de escuelas por localidad en pdf

## Próximos proyectos:
### Completar manejo de excepciones
### Redis. Cargar los datos y accederlos
### Utilizando en ORM, cambiar el motor de base de datos

La base de datos se basa en un archivo csv que contiene
todas las escuelas del país a una cierta fecha.

[Se puede obtener acá](https://www.argentina.gob.ar/sites/default/files/mae_actualizado_2019-09-16_envios.zip)

Hay que descomprimirlo y seguir los pasos que se detallan a continuación.

### Para crear las tablas:

#### El modelo de datos del ORM: model/db.py

### 1. Load del .csv
```
(venv)$ sqlite3 escuelas.db
SQLite version 3.29.0 2019-07-10 17:32:03
Enter ".help" for usage hints.
sqlite> .mode csv DatosBase
sqlite> .import ./sql/data/DatosBase.csv DatosBase
sqlite> select count(*) from DatosBase;
63390
sqlite> .quit
(venv) juan@xubuntu:~/dev/python/sqlesc/db$ ls -l
total 14612
-rw-r--r-- 1 juan juan 14962688 may 29 15:21 escuelas.db
```

### 2. Crear tablas
```
(venv)$ sqlite3 escuelas.db
sqlite> .read ./sql/tables/Sector.sql
sqlite> .read ./sql/tables/Ambito.sql
sqlite> .read ./sql/tables/Provincia.sql
sqlite> .read ./sql/tables/Localidad.sql
sqlite> .read ./sql/tables/Escuela.sql
sqlite> .read ./sql/tables/DomicilioEscuela.sql
sqlite> .read ./sql/tables/NivelEducacion.sql
sqlite> .read ./sql/tables/TipoEducacion.sql
sqlite> .read ./sql/tables/TipoNivelEducacion.sql
sqlite> .read ./sql/tables/TedNivEscuela.sql
```

### 3. Cargar Datos Básicos
```
sqlite> .read ./sql/load/sectores.sql
sqlite> .read ./sql/load/ambitos.sql
sqlite> .read ./sql/load/provincias.sql
sqlite> .read ./sql/load/departamento.sql
sqlite> .read ./sql/load/localidades.sql
update DatosBase set Ámbito = 'Sin Información' where "CUE Anexo" in ('062304200','062309200','062309500');
sqlite> .read ./sql/tables/escuelas.sql
sqlite> .read ./sql/tables/domicilioescuelas.sql
sqlite> .read ./sql/load/niveleseducacion.sql
sqlite> .read ./sql/load/tiposeducacion.sql
sqlite> .read ./sql/load/tiposniveleseducacion.sql
```

### 4. Crear Views
```
sqlite> .read ./sql/views/adultos.sql
sqlite> .read ./sql/views/arte.sql
sqlite> .read ./sql/views/bilingue.sql
sqlite> .read ./sql/views/comun.sql
sqlite> .read ./sql/views/encierro.sql
sqlite> .read ./sql/views/especial.sql
sqlite> .read ./sql/views/hospital.sql
sqlite> .read ./sql/views/servicios.sql
```

### 5. Cargar Datos Educación
```
sqlite> .read ./sql/load/tednivescuelas.sql
```

## Listado para crear las tablas
```
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE IF NOT EXISTS "Persona" (
	id INTEGER NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "Ambito" (
	id INTEGER NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "Sector" (
	id INTEGER NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "Provincia" (
	id INTEGER NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "TipoEducacion" (
	id INTEGER NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "NivelEducacion" (
	id INTEGER NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "Usuario" (
	id INTEGER NOT NULL, 
	email VARCHAR(128), 
	password_hash VARCHAR(128), 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX "ix_Usuario_email" ON "Usuario" (email);
CREATE TABLE IF NOT EXISTS "Domicilio" (
	id INTEGER NOT NULL, 
	numero VARCHAR(255) NOT NULL, 
	codpos VARCHAR(255) NOT NULL, 
	calle VARCHAR(255) NOT NULL, 
	persona_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(persona_id) REFERENCES "Persona" (id)
);
CREATE TABLE IF NOT EXISTS "Localidad" (
	id INTEGER NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	codigo VARCHAR(32) NOT NULL, 
	provincia_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(provincia_id) REFERENCES "Provincia" (id)
);
CREATE TABLE IF NOT EXISTS "TipoNivelEducacion" (
	id INTEGER NOT NULL, 
	tipoeducacion_id INTEGER, 
	niveleducacion_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tipoeducacion_id) REFERENCES "TipoEducacion" (id), 
	FOREIGN KEY(niveleducacion_id) REFERENCES "NivelEducacion" (id)
);
CREATE TABLE IF NOT EXISTS "Escuela" (
	id INTEGER NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	codigo VARCHAR(32) NOT NULL, 
	sector_id INTEGER, 
	ambito_id INTEGER, 
	localidad_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sector_id) REFERENCES "Sector" (id), 
	FOREIGN KEY(ambito_id) REFERENCES "Ambito" (id), 
	FOREIGN KEY(localidad_id) REFERENCES "Localidad" (id)
);
CREATE TABLE IF NOT EXISTS "DomicilioEscuela" (
	id INTEGER NOT NULL, 
	numero VARCHAR(255) NOT NULL, 
	codpos VARCHAR(255) NOT NULL, 
	calle VARCHAR(255) NOT NULL, 
	escuela_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(escuela_id) REFERENCES "Escuela" (id)
);
CREATE TABLE IF NOT EXISTS "TedNivEscuela" (
	id INTEGER NOT NULL, 
	escuela_id INTEGER, 
	"tipoNivelEducacion_id" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(escuela_id) REFERENCES "Escuela" (id), 
	FOREIGN KEY("tipoNivelEducacion_id") REFERENCES "TipoNivelEducacion" (id)
);
CREATE TABLE DatosBase(
  "Jurisdicción" TEXT,
  "CUE Anexo" TEXT,
  "Nombre" TEXT,
  "Sector" TEXT,
  "Ámbito" TEXT,
  "Domicilio" TEXT,
  "CP" TEXT,
  "Código de área" TEXT,
  "Teléfono" TEXT,
  "Código localidad" TEXT,
  "Localidad" TEXT,
  "Departamento" TEXT,
  "Mail" TEXT,
  "Ed. Común" TEXT,
  "Ed. Especial" TEXT,
  "Ed. Adultos" TEXT,
  "Ed. Artística" TEXT,
  "Ed. Hospitalaria Domiciliaria" TEXT,
  "Ed. Intercultural Bilingüe" TEXT,
  "Ed. Contexto de Encierro" TEXT,
  "Ed. Común Jardín maternal" TEXT,
  "Ed. Común Inicial" TEXT,
  "Ed. Común Primaria" TEXT,
  "Ed. Común Secundaria" TEXT,
  "Ed. Común Secundaria Técnica (INET)" TEXT,
  "Ed. Común Superior no Universitario" TEXT,
  "Ed. Común Superior No Universitario (INET)" TEXT,
  "Ed. Artística Secundaria" TEXT,
  "Ed. Artística Superior no Universitario" TEXT,
  "Ed. Artística Cursos y Talleres" TEXT,
  "Ed. Especial Educación Temprana" TEXT,
  "Ed. Especial Inicial" TEXT,
  "Ed. Especial Primaria" TEXT,
  "Ed. Especial Secundaria" TEXT,
  "Ed. Especial Integración" TEXT,
  "Ed. Adultos Primaria" TEXT,
  "Ed. Adultos EGB3" TEXT,
  "Ed. Adultos Secundaria" TEXT,
  "Ed. Adultos Alfabetización" TEXT,
  "Ed. Adultos Formación Profesional" TEXT,
  "Ed. Adultos Formación Profesional (INET)" TEXT,
  "Ed. Hospitalaria Domiciliaria Inicial" TEXT,
  "Ed. Hospitalaria Domiciliaria Primaria" TEXT,
  "Ed. Hospitalaria Domiciliaria Secundaria" TEXT,
  "Servicios complementarios" TEXT
);

```
## Crear las vistas.
Se usan para armar las tablas de niveles y tipos de educación de
cada escuela.

```
CREATE VIEW Adultos as
          select  1 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Común Jardin maternal" = 'X'             
union all select  2 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Común Inicial"    = 'X'                     
union all select  3 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Común Primaria"         = 'X'               
union all select  4 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Común Secundaria"            = 'X'         
union all select  5 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Común Secundaria Tecnica INET"      = 'X'   
union all select  6 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Común Superior no Universitario"     = 'X' 
union all select  7 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Común Superior No Universitario INET" = 'X' 
union all select 46 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Artística Secundaria"                 = 'X' 
union all select 48 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Artística Superior no Universitario"  = 'X' 
union all select 50 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Artística Cursos y Talleres"          = 'X' 
union all select 23 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Especial Educación Temprana"          = 'X' 
union all select 17 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Especial Inicial"                     = 'X' 
union all select 18 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Especial Primaria"                    = 'X' 
union all select 19 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Especial Secundaria"                  = 'X' 
union all select 24 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Especial Integración"                 = 'X' 
union all select 31 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Adultos Primaria"                     = 'X' 
union all select 39 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Adultos EGB3"                         = 'X' 
union all select 32 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Adultos Secundaria"                   = 'X' 
union all select 40 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Adultos Alfabetizacion"               = 'X' 
union all select 41 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Adultos Formacion Profesional"        = 'X' 
union all select 42 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Adultos Formacion Profesional INET"   = 'X' 
union all select 58 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Hospitalaria Domiciliaria Inicial"    = 'X' 
union all select 59 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Hospitalaria Domiciliaria Primaria"   = 'X' 
union all select 60 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Adultos" = 'X' and "Ed. Hospitalaria Domiciliaria Secundaria" = 'X'
/* Adultos(idTN,Codigo) */;
CREATE VIEW Arte as
          select  1 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Común Jardin maternal" = 'X'             
union all select  2 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Común Inicial"    = 'X'                     
union all select  3 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Común Primaria"         = 'X'               
union all select  4 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Común Secundaria"            = 'X'         
union all select  5 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Común Secundaria Tecnica INET"      = 'X'   
union all select  6 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Común Superior no Universitario"     = 'X' 
union all select  7 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Común Superior No Universitario INET" = 'X' 
union all select 46 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Artística Secundaria"                 = 'X' 
union all select 48 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Artística Superior no Universitario"  = 'X' 
union all select 50 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Artística Cursos y Talleres"          = 'X' 
union all select 23 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Especial Educación Temprana"          = 'X' 
union all select 17 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Especial Inicial"                     = 'X' 
union all select 18 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Especial Primaria"                    = 'X' 
union all select 19 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Especial Secundaria"                  = 'X' 
union all select 24 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Especial Integración"                 = 'X' 
union all select 31 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Adultos Primaria"                     = 'X' 
union all select 39 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Adultos EGB3"                         = 'X' 
union all select 32 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Adultos Secundaria"                   = 'X' 
union all select 40 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Adultos Alfabetizacion"               = 'X' 
union all select 41 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Adultos Formacion Profesional"        = 'X' 
union all select 42 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Adultos Formacion Profesional INET"   = 'X' 
union all select 58 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Hospitalaria Domiciliaria Inicial"    = 'X' 
union all select 59 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Hospitalaria Domiciliaria Primaria"   = 'X' 
union all select 60 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Artística" = 'X' and "Ed. Hospitalaria Domiciliaria Secundaria" = 'X'
/* Arte(idTN,Codigo) */;
CREATE VIEW Bilingue as
          select 1 as idTN,  "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Común Jardin maternal" = 'X'             
union all select 2 as idTN,  "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Común Inicial"    = 'X'                     
union all select 3 as idTN,  "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Común Primaria"         = 'X'               
union all select 4 as idTN,  "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Común Secundaria"            = 'X'         
union all select 5 as idTN,  "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Común Secundaria Tecnica INET"      = 'X'   
union all select 6 as idTN,  "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Común Superior no Universitario"     = 'X' 
union all select 7 as idTN,  "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Común Superior No Universitario INET" = 'X' 
union all select 46 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Artística Secundaria"                 = 'X' 
union all select 48 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Artística Superior no Universitario"  = 'X' 
union all select 50 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Artística Cursos y Talleres"          = 'X' 
union all select 23 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Especial Educación Temprana"          = 'X' 
union all select 17 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Especial Inicial"                     = 'X' 
union all select 18 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Especial Primaria"                    = 'X' 
union all select 19 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Especial Secundaria"                  = 'X' 
union all select 24 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Especial Integración"                 = 'X' 
union all select 31 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Adultos Primaria"                     = 'X' 
union all select 39 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Adultos EGB3"                         = 'X' 
union all select 32 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Adultos Secundaria"                   = 'X' 
union all select 40 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Adultos Alfabetizacion"               = 'X' 
union all select 41 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Adultos Formacion Profesional"        = 'X' 
union all select 42 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Adultos Formacion Profesional INET"   = 'X' 
union all select 58 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Hospitalaria Domiciliaria Inicial"    = 'X' 
union all select 59 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Hospitalaria Domiciliaria Primaria"   = 'X' 
union all select 60 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Intercultural Bilingüe" = 'X' and "Ed. Hospitalaria Domiciliaria Secundaria" = 'X'
/* Bilingue(idTN,Codigo) */;
CREATE VIEW Comun as
          select  1 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Común Jardin maternal" = 'X'             
union all select  2 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Común Inicial"    = 'X'                     
union all select  3 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Común Primaria"         = 'X'               
union all select  4 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Común Secundaria"            = 'X'         
union all select  5 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Común Secundaria Tecnica INET"      = 'X'   
union all select  6 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Común Superior no Universitario"     = 'X' 
union all select  7 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Común Superior No Universitario INET" = 'X' 
union all select 46 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Artística Secundaria"                 = 'X' 
union all select 48 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Artística Superior no Universitario"  = 'X' 
union all select 50 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Artística Cursos y Talleres"          = 'X' 
union all select 23 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Especial Educación Temprana"          = 'X' 
union all select 17 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Especial Inicial"                     = 'X' 
union all select 18 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Especial Primaria"                    = 'X' 
union all select 19 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Especial Secundaria"                  = 'X' 
union all select 24 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Especial Integración"                 = 'X' 
union all select 31 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Adultos Primaria"                     = 'X' 
union all select 39 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Adultos EGB3"                         = 'X' 
union all select 32 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Adultos Secundaria"                   = 'X' 
union all select 40 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Adultos Alfabetizacion"               = 'X' 
union all select 41 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Adultos Formacion Profesional"        = 'X' 
union all select 42 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Adultos Formacion Profesional INET"   = 'X' 
union all select 58 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Hospitalaria Domiciliaria Inicial"    = 'X' 
union all select 59 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Hospitalaria Domiciliaria Primaria"   = 'X' 
union all select 60 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Común" = 'X' and "Ed. Hospitalaria Domiciliaria Secundaria" = 'X'
/* Comun(idTN,Codigo) */;
CREATE VIEW Encierro as
          select  1 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Común Jardin maternal" = 'X'             
union all select  2 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Común Inicial"    = 'X'                     
union all select  3 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Común Primaria"         = 'X'               
union all select  4 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Común Secundaria"            = 'X'         
union all select  5 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Común Secundaria Tecnica INET"      = 'X'   
union all select  6 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Común Superior no Universitario"     = 'X' 
union all select  7 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Común Superior No Universitario INET" = 'X' 
union all select 46 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Artística Secundaria"                 = 'X' 
union all select 48 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Artística Superior no Universitario"  = 'X' 
union all select 50 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Artística Cursos y Talleres"          = 'X' 
union all select 23 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Especial Educación Temprana"          = 'X' 
union all select 17 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Especial Inicial"                     = 'X' 
union all select 18 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Especial Primaria"                    = 'X' 
union all select 19 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Especial Secundaria"                  = 'X' 
union all select 24 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Especial Integración"                 = 'X' 
union all select 31 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Adultos Primaria"                     = 'X' 
union all select 39 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Adultos EGB3"                         = 'X' 
union all select 32 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Adultos Secundaria"                   = 'X' 
union all select 40 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Adultos Alfabetizacion"               = 'X' 
union all select 41 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Adultos Formacion Profesional"        = 'X' 
union all select 42 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Adultos Formacion Profesional INET"   = 'X' 
union all select 58 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Hospitalaria Domiciliaria Inicial"    = 'X' 
union all select 59 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Hospitalaria Domiciliaria Primaria"   = 'X' 
union all select 60 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Contexto de Encierro" = 'X' and "Ed. Hospitalaria Domiciliaria Secundaria" = 'X'
/* Encierro(idTN,Codigo) */;
CREATE VIEW Especial as
          select  1 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Común Jardin maternal" = 'X'             
union all select  2 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Común Inicial"    = 'X'                     
union all select  3 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Común Primaria"         = 'X'               
union all select  4 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Común Secundaria"            = 'X'         
union all select  5 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Común Secundaria Tecnica INET"      = 'X'   
union all select  6 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Común Superior no Universitario"     = 'X' 
union all select  7 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Común Superior No Universitario INET" = 'X' 
union all select 46 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Artística Secundaria"                 = 'X' 
union all select 48 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Artística Superior no Universitario"  = 'X' 
union all select 50 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Artística Cursos y Talleres"          = 'X' 
union all select 23 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Especial Educación Temprana"          = 'X' 
union all select 17 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Especial Inicial"                     = 'X' 
union all select 18 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Especial Primaria"                    = 'X' 
union all select 19 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Especial Secundaria"                  = 'X' 
union all select 24 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Especial Integración"                 = 'X' 
union all select 31 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Adultos Primaria"                     = 'X' 
union all select 39 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Adultos EGB3"                         = 'X' 
union all select 32 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Adultos Secundaria"                   = 'X' 
union all select 40 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Adultos Alfabetizacion"               = 'X' 
union all select 41 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Adultos Formacion Profesional"        = 'X' 
union all select 42 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Adultos Formacion Profesional INET"   = 'X' 
union all select 58 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Hospitalaria Domiciliaria Inicial"    = 'X' 
union all select 59 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Hospitalaria Domiciliaria Primaria"   = 'X' 
union all select 60 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Especial" = 'X' and "Ed. Hospitalaria Domiciliaria Secundaria" = 'X'
/* Especial(idTN,Codigo) */;
CREATE VIEW Hospital as
          select  1 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Común Jardin maternal" = 'X'             
union all select  2 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Común Inicial"    = 'X'                     
union all select  3 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Común Primaria"         = 'X'               
union all select  4 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Común Secundaria"            = 'X'         
union all select  5 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Común Secundaria Tecnica INET"      = 'X'   
union all select  6 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Común Superior no Universitario"     = 'X' 
union all select  7 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Común Superior No Universitario INET" = 'X' 
union all select 46 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Artística Secundaria"                 = 'X' 
union all select 48 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Artística Superior no Universitario"  = 'X' 
union all select 50 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Artística Cursos y Talleres"          = 'X' 
union all select 23 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Especial Educación Temprana"          = 'X' 
union all select 17 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Especial Inicial"                     = 'X' 
union all select 18 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Especial Primaria"                    = 'X' 
union all select 19 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Especial Secundaria"                  = 'X' 
union all select 24 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Especial Integración"                 = 'X' 
union all select 31 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Adultos Primaria"                     = 'X' 
union all select 39 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Adultos EGB3"                         = 'X' 
union all select 32 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Adultos Secundaria"                   = 'X' 
union all select 40 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Adultos Alfabetizacion"               = 'X' 
union all select 41 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Adultos Formacion Profesional"        = 'X' 
union all select 42 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Adultos Formacion Profesional INET"   = 'X' 
union all select 58 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Hospitalaria Domiciliaria Inicial"    = 'X' 
union all select 59 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Hospitalaria Domiciliaria Primaria"   = 'X' 
union all select 60 as idTN, "CUE Anexo" as Codigo from DatosBase where "Ed. Hospitalaria Domiciliaria" = 'X' and "Ed. Hospitalaria Domiciliaria Secundaria" = 'X'
/* Hospital(idTN,Codigo) */;
CREATE VIEW Servicios as
          select  1 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Común Jardin maternal" = 'X'             
union all select  2 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Común Inicial"    = 'X'                     
union all select  3 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Común Primaria"         = 'X'               
union all select  4 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Común Secundaria"            = 'X'         
union all select  5 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Común Secundaria Tecnica INET"      = 'X'   
union all select  6 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Común Superior no Universitario"     = 'X' 
union all select  7 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Común Superior No Universitario INET" = 'X' 
union all select 46 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Artística Secundaria"                 = 'X' 
union all select 48 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Artística Superior no Universitario"  = 'X' 
union all select 50 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Artística Cursos y Talleres"          = 'X' 
union all select 23 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Especial Educación Temprana"          = 'X' 
union all select 17 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Especial Inicial"                     = 'X' 
union all select 18 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Especial Primaria"                    = 'X' 
union all select 19 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Especial Secundaria"                  = 'X' 
union all select 24 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Especial Integración"                 = 'X' 
union all select 31 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Adultos Primaria"                     = 'X' 
union all select 39 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Adultos EGB3"                         = 'X' 
union all select 32 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Adultos Secundaria"                   = 'X' 
union all select 40 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Adultos Alfabetizacion"               = 'X' 
union all select 41 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Adultos Formacion Profesional"        = 'X' 
union all select 42 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Adultos Formacion Profesional INET"   = 'X' 
union all select 58 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Hospitalaria Domiciliaria Inicial"    = 'X' 
union all select 59 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Hospitalaria Domiciliaria Primaria"   = 'X' 
union all select 60 as idTN, "CUE Anexo" as Codigo from DatosBase where "Servicios complementarios" = 'X' and "Ed. Hospitalaria Domiciliaria Secundaria" = 'X'
/* Servicios(idTN,Codigo) */;

```
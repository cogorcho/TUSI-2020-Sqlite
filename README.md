# SQLITE

### Para crear las tablas:
```
python model/db.py 
```

```
(venv) juan@xubuntu:~/dev/python/sqlesc/db$ sqlite3 escuelas.db
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

## Crear tablas
```
(venv) juan@xubuntu:~/dev/python/sqlesc/db$ sqlite3 escuelas.db
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

## Cargar Datos Básicos
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

## Crear Views
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

## Cargar Datos Educación
```
sqlite> .read ./sql/load/tednivescuelas.sql
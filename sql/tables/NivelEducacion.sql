-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: NivelEducacion
-- --------------------------------------
drop table if exists NivelEducacion;

create table NivelEducacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre varchar(256) not null
);

create unique index uidx_NivelEducacion
on NivelEducacion(nombre);
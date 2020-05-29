-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: TipoEducacion
-- --------------------------------------
create table TipoEducacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre varchar(256) not null
);

create unique index uidx_TipoEducacion
on TipoEducacion(nombre);
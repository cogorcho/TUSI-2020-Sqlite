-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: Ambito
-- --------------------------------------
create table Ambito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre varchar(256) not null
);

create unique index uidx_Ambito
on Ambito(nombre);
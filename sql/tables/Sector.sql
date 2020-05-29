-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: Sector
-- --------------------------------------
create table Sector (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre varchar(256) not null
);

create unique index uidx_Sector
on Sector(nombre);
-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: Provincia 
-- --------------------------------------
create table if not exists Provincia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre varchar(128) NOT NULL
);

create unique index uidx_Provincia on Provincia(nombre);
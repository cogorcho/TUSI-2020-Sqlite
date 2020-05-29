-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: Localidad
-- --------------------------------------
create table Localidad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idProvincia INT NOT NULL,
    codigo varchar(32) NOT NULL,
    nombre varchar(256) not null,
    CONSTRAINT fk_localidad_pcia foreign key (idProvincia) references Provincia(id)
);

create unique index uidx_Localidad
on Localidad(idProvincia, codigo, nombre);
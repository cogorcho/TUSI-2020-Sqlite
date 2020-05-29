-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: Departamento
-- --------------------------------------
create table Departamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idProvincia INT NOT NULL,
    nombre varchar(256) not null,
    CONSTRAINT fk_depto_pcia foreign key (idProvincia)
    references Provincia(id)
);

create unique index uidx_Departamento
on Departamento(idProvincia, nombre);
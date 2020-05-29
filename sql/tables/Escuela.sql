-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: Escuela
-- --------------------------------------
create table Escuela (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idLocalidad INT NOT NULL,
    idSector INT NOT NULL,
    idAmbito INT NOT NULL,
    codigo varchar(32) NOT NULL,
    nombre varchar(256) not null,
    domicilio varchar(256) not null,
    codpos varchar(64),
    CONSTRAINT fk_escuela_sector foreign key (idSector) references Sector(id),
    CONSTRAINT fk_escuela_localidad foreign key (idLocalidad) references Localidad(id),
    CONSTRAINT fk_escuela_ambito foreign key (idAmbito) references Ambito(id)
);


create unique index uidx_escuela_codigo
on Escuela(codigo);

-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DDL: Create table
-- Tabla: NivelEducacion
-- --------------------------------------
drop table if exists TipoNivelEducacion;

create table TipoNivelEducacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idTipoEducacion INT NOT NULL,
    idNivelEducacion INT NOT NULL,
    CONSTRAINT fk_nte_te FOREIGN KEY (idTipoEducacion) REFERENCES TipoEducacion(id),
    CONSTRAINT fk_nte_niv FOREIGN KEY (idNivelEducacion) REFERENCES NivelEducacion(id)
);

create unique index uidx_TipoNivelEducacion
on TipoNivelEducacion(idTipoEducacion,idNivelEducacion);

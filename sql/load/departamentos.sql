-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DML: Insert into table
-- Tabla: Departamento
-- Generar data, esta vez con FK 
-- --------------------------------------
insert into Departamento (idProvincia, nombre)
select distinct Provincia.id, DatosBase.Departamento
from DatosBase
inner join Provincia on Provincia.nombre = DatosBase.Jurisdicción
order by Provincia.id, DatosBase.Departamento;

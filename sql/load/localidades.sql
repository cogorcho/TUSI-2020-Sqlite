-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DML: Insert into table
-- Tabla: Localidad
-- Generar data, FK 
-- --------------------------------------
insert into Localidad(provincia_id, codigo, nombre)
select distinct Provincia.id, DatosBase."Código Localidad", DatosBase.Localidad
from DatosBase
inner join Provincia
on Provincia.nombre = DatosBase.Jurisdicción
order by 1,2,3;

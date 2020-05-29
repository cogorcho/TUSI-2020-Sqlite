-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DML: Insert rows into table
-- Tabla: Provincia 
-- Con un select a DatosBase generamos 
-- detos de provincias, ordenados.
-- --------------------------------------
insert into Provincia(nombre)
select distinct Jurisdicción 
from DatosBase 
order by Jurisdicción;
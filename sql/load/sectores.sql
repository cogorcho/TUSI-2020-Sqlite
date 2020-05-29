-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DML: Insert into table
-- Tabla: Sector
-- Generar data, esta vez con FK 
-- --------------------------------------
insert into Sector (nombre)
select distinct Sector
from DatosBase;
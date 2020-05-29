-- --------------------------------------
-- TSSI-2020. administracion de BD
-- DML: Insert into table
-- Tabla: Sector
-- Generar data, esta vez con FK 
-- --------------------------------------
insert into Ambito (nombre)
select distinct 
case 
    length(Ámbito) when 0 then 'Sin Información' 
    else Ámbito 
end as nombre 
from DatosBase;
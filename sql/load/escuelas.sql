insert into Escuela
(localidad_id,sector_id,ambito_id,codigo,nombre)     
select l.id, a.id, s.id, b."CUE Anexo", b.nombre
from DatosBase b 
inner join Provincia p
on p.nombre = b.Jurisdicción
inner join Localidad l
on l.nombre = b.localidad
and l.codigo = b."código localidad"
inner join Sector s
on s.nombre = b.sector
inner join Ambito a
on a.nombre = b.Ámbito;


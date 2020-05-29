insert into TedNivEscuela (idEscuela, idTipoNivel)
select escu.id, v.idTN
from Escuela escu
inner join Comun v
    on v.Codigo = escu.Codigo
union
select escu.id, v.idTN
from Escuela escu
inner join Especial v
    on v.Codigo = escu.Codigo
union
select escu.id, v.idTN
from Escuela escu
inner join Adultos v
    on v.Codigo = escu.Codigo
union
select escu.id, v.idTN
from Escuela escu
inner join Arte v
    on v.Codigo = escu.Codigo
union
select escu.id, v.idTN
from Escuela escu
inner join Bilingue v
    on v.Codigo = escu.Codigo
union
select escu.id, v.idTN
from Escuela escu
inner join Hospital v
    on v.Codigo = escu.Codigo
union
select escu.id, v.idTN
from Escuela escu
inner join Encierro v
    on v.Codigo = escu.Codigo
union
select escu.id, v.idTN
from Escuela escu
inner join Servicios v
    on v.Codigo = escu.Codigo;
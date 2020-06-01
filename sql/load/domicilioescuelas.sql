insert into "DomicilioEscuela"(
    numero, codpos, calle, escuela_id
)
select 0, daba.cp, daba.domicilio, escu.id 
from Datosbase daba
inner join Escuela escu
on escu.codigo = daba."CUE Anexo";
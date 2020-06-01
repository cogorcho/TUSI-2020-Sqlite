insert into TipoNivelEducacion (tipoEducacion_id, nivelEducacion_id)
select te.id, ni.id
from TipoEducacion te, NivelEducacion ni 
order by 1,2;
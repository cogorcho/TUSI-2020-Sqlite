drop table if exists MailTel;

create table MailTel (
    id int not null,
    Codigo varchar(32), 
    telefono varchar(128), 
    mail varchar(255)
)
as
select e.id, db.CUE_Anexo as Codigo, lower(trim(db.Mail)) as Mail,
concat('(',db.Codigo_de_area,')',trim(db.telefono)) as Telefono
from DatosBase db
inner join Escuela e
 on e.Codigo = db.CUE_Anexo;

ALTER TABLE MailTel ADD PRIMARY KEY(id);

create unique index uidx_MailTel on MailTel(Codigo)




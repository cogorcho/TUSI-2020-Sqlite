CREATE TABLE DOMICILIO (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CALLE VARCHAR(255),
    NUMERO VARCHAR(64),
    CODPOS VARCHAR(32)
    IDPERSONA INTEGER NOT NULL,
    FOREIGN KEY (FK_DOM_PERS) IDPERSONA REFERENCES PERSONA(ID)
)
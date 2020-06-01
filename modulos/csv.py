import os

class CSV():
    def __init__(self, csvfile=None):
        if csvfile is None:
            self.csvfile = './sql/data/DatosBase.csv'
            self.data = []

    def gentab(self):
        try:
            with open(self.csvfile) as fp:
                linea = fp.readline()
                sql = self.gencreate(linea)
                fp.close()
                return sql
        except Exception as e:
            print("Error abriendo %s [%s]" %(self.csvfile, str(e)))

    def gencreate(self, linea):
        ncols = linea.strip().replace('(','').replace(')','').replace('Á','A').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u').replace('.','').replace(' ','_').split(',')
        sql = 'CREATE TABLE DatosBase ('
        cnt = 1
        for c in ncols:
            if cnt == 1:
                sql += "%s TEXT" % (c)
                cnt = 2
            else:
                sql += ", %s TEXT" % (c) 
        sql += ')'       
        return sql


    def getcols(self, linea):
        rec = []
        estado = 0
        campo = ""
        for c in linea:
            if c == ',':
                if estado == 0:
                    rec.append(campo.strip())
                    campo = ""
                else:
                    campo += c
            elif c == '"':
                if estado == 2:
                    estado = 0
                else:
                    estado = 2
            else:
                campo += c
        return rec

    def genrows(self):
        lcnt = 1
        data = []
        try:
            with open(self.csvfile) as fp:
                linea = fp.readline()
                while linea:
                    if lcnt == 1:
                        lcnt = 2
                        continue
                    else:
                        data.append(self.getcols(linea))
                    linea = fp.readline()
                fp.close()
                return data
        except Exception as e:
            print("Error abriendo %s [%s]" %(self.csvfile, str(e)))



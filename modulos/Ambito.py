class Ambito():
    def __init__(self):
        print("Ambito")

    def getId(self, nombre):
        sql = "select id from Ambito where id = {}".format(nombre)
        try:
            c = conn.cursor()
            c.execute(sql)
            return c.fetchone()
        except Exception as e:
            print("Error buscando Ambito (%s) : %s" % (nombre, str(e)))
            return -1
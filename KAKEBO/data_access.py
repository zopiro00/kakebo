import sqlite3

def modificaSQL(query, parametros=[]):
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()
    cur.execute(query, parametros)

    conexion.commit()
    conexion.close

def calcularSaldo(movimientos):
    saldo = 0
    for d in movimientos:
        if d['esGasto'] == 0:
            saldo = saldo + float(d['cantidad'])
        else:
            saldo = saldo - float(d['cantidad'])
        d['saldo'] = saldo
    return movimientos



class DBmanager():
    def __toDict__(self, cur):
        claves = cur.description
        filas = cur.fetchall()

        l = []
        for fila in filas:
            d = {}
            for tclave, valor in zip(claves, fila):
                d[tclave[0]] = valor
            l.append(d)
        return l

    def modificaSQL(self, query, parametros=[]):
        conexion = sqlite3.connect("movimientos.db")
        cur = conexion.cursor()

        cur.execute(query, parametros)

        conexion.commit()
        conexion.close

    def consultaMuchasSQL(self, query, parametros=[]):
        pass
    def consultaUnaSQL(self, query, parametros=[]):
        pass

    def consultaSQL(self, query, parametros=[]):
        #Abrimos conexion
        conexion = sqlite3.connect("movimientos.db")
        cur = conexion.cursor()

        #Ejecutamos consulta
        cur.execute(query, parametros)

        #Procesamos datos para devolver una lista de diccionarios.
        claves = cur.description
        filas = cur.fetchall()
        l = []

        for fila in filas:
            d = {}
            for tclave, valor in zip(claves, fila):
                d[tclave[0]] = valor
            l.append(d)

        # Cierro servidor.
        conexion.close()

        #Devuelvo los datos.
        return l
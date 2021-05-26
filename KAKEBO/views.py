from KAKEBO import app
import sqlite3
from flask import jsonify, render_template, request
from KAKEBO.forms import MovimientosForm

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()
    cur.execute("SELECT * FROM movimientos;")

    claves = cur.description
    filas = cur.fetchall()
    l = []
    saldo = 0

    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
            print(d)
        if d['esGasto'] == 0:
            saldo = saldo + float(d['cantidad'])
        else:
            saldo = saldo - float(d['cantidad'])
        d['saldo'] = saldo
        l.append(d)

    conexion.close()
    #print(l)

    #return jsonify(l)
    return render_template("movimientos.html", datos = l )

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    form = MovimientosForm()
    return render_template('alta.html', form = form)


from flask.helpers import url_for
from KAKEBO import app
import sqlite3
from flask import jsonify, render_template, request, redirect, url_for

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

    if request.method == "GET":
        return render_template('alta.html', form = form)

    else: # if POST
        if form.validate():
            conexion = sqlite3.connect("movimientos.db")
            cur = conexion.cursor()

            query=  """
                    INSERT INTO movimientos (fecha,concepto,categoria, esGasto, cantidad) VALUES(?,?,?,?,?)
                    """
            #Las interrogaciones se utilizan en SQL como huecos que rellenar.
            try:
                cur.execute(query, [form.fecha.data,
                                    form.concepto.data,
                                    form.categoria.data,
                                    form.esGasto.data,
                                    form.cantidad.data])
            except sqlite3.Error as el_error:
                print(el_error)
                return render_template("alta.html", form = form)
            conexion.commit()
            conexion.close
            #Volver a la página principal
            #return redirect("/")
            return redirect(url_for("index"))
        else:
            return render_template('alta.html', form = form)

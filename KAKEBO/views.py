from flask.helpers import url_for
from KAKEBO import app
import sqlite3
from flask import jsonify, render_template, request, redirect, url_for, flash
from datetime import date
from KAKEBO.forms import MovimientosForm

def consultaSQL(query, parametros=[]):
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

def modificaSQL(query, parametros=[]):
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()
    cur.execute(query, parametros)

    conexion.commit()
    conexion.close

@app.route('/')
def index():
    movimientos = consultaSQL("SELECT * FROM movimientos;")
    saldo = 0

    for d in movimientos:
        if d['esGasto'] == 0:
            saldo = saldo + float(d['cantidad'])
        else:
            saldo = saldo - float(d['cantidad'])
        d['saldo'] = saldo

    return render_template("movimientos.html", datos = movimientos )

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    form = MovimientosForm()

    if request.method == "GET":
        return render_template('alta.html', form = form)

    else: # if POST
        if form.validate():
            query=  """
                    INSERT INTO movimientos (fecha,concepto,categoria, esGasto, cantidad) VALUES(?,?,?,?,?)
                    """
            #Las interrogaciones se utilizan en SQL como huecos que rellenar.
            try:
                modificaSQL(query, [form.fecha.data,
                                    form.concepto.data,
                                    form.categoria.data,
                                    form.esGasto.data,
                                    form.cantidad.data])
            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                flash("se ha producido un error en la base de datos. Pruebe en unos minutos.", "alert")
                return render_template("alta.html", form = form)

            #Volver a la página principal
            return redirect(url_for("index"))

        else:
            return render_template('alta.html', form = form)

@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    formulario = MovimientosForm()
    if request.method == "GET":
        filas = consultaSQL("SELECT * FROM movimientos WHERE id= ?", [id])
        if len(filas) == 0:
            flash("No se encuentra el movimiento.", "alert")
            return render_template('borrar.html', form = None)
    else:
        if formulario.submit.data:
            try:
                modificaSQL("DELETE FROM movimientos WHERE id = ?;", [id])
            except sqlite3.error as e:
                flash("Se ha producido un error de base de datos, vuelva a intentarlo", 'error')
                return redirect(url_for('index'))
                
            flash("Borrado realizado con éxito", 'mensaje')    
            return redirect(url_for('index'))
        elif formulario.Nosubmit.data:
            flash("Borrado Anulado", 'mensaje')    
            return redirect(url_for('index'))

    registro = filas[0]
    registro["fecha"] = date.fromisoformat(registro["fecha"])
    formulario = MovimientosForm(data = registro)
    return render_template('borrar.html', form = formulario, id = id)

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):

    query = """
            UPDATE movimientos SET fecha=?, concepto=?, categoria=?,esGasto=?, cantidad=? WHERE id=? 
            """
    form = MovimientosForm()
    if request.method == "GET":
        filas = consultaSQL("SELECT * FROM movimientos WHERE id= ?", [id])
        if len(filas) == 0:
            flash("No se encuentra el movimiento.", "alert")
            return render_template('modificar.html', form = None)
    else:
        if form.submit.data:
            try:
                modificaSQL(query, [form.fecha.data,
                                    form.concepto.data,
                                    form.categoria.data,
                                    form.esGasto.data,
                                    form.cantidad.data,
                                    id])
            except sqlite3.error as e:
                flash("Se ha producido un error de base de datos, vuelva a intentarlo", 'error')
                return redirect(url_for('index'))
                
            flash("Modificación realizada con éxito", 'mensaje')    
            return redirect(url_for('index'))
        elif form.Nosubmit.data:
            flash("Modificación Anulada", 'mensaje')    
            return redirect(url_for('index'))

    registro = filas[0]
    registro["fecha"] = date.fromisoformat(registro["fecha"])
    form = MovimientosForm(data = registro)
    return render_template('modificar.html', form = form, id = id)


    

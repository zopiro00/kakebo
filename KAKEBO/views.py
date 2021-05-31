from flask.helpers import url_for
from KAKEBO import app
import sqlite3
from flask import jsonify, render_template, request, redirect, url_for, flash
from datetime import date
from KAKEBO.forms import Filtrar, MovimientosForm

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

def calcularSaldo(movimientos):
    saldo = 0
    for d in movimientos:
        if d['esGasto'] == 0:
            saldo = saldo + float(d['cantidad'])
        else:
            saldo = saldo - float(d['cantidad'])
        d['saldo'] = saldo
    return movimientos

@app.route('/')
@app.route('/<desde>', methods=['GET', 'POST'])
def index(desde = "None"):
    filtrar = Filtrar()

    if request.method == "GET":
        movimientos = consultaSQL("SELECT * FROM movimientos;")
    else:
        if filtrar.reset.data == True:
            return redirect(url_for('index'))
        if filtrar.submit.data == True:
            if desde:
                query = """
                        SELECT * FROM movimientos WHERE fecha=?;
                        """        
                movimientos = consultaSQL(query, [desde])
                flash("Se ha filtrado por por los valores definidos", "mensaje")

    movimientoConSaldo = calcularSaldo(movimientos)

    return render_template("movimientos.html", datos = movimientoConSaldo, filtrar = filtrar)

"""
elif not texto:
    query = ""
            SELECT * FROM movimientos WHERE fecha > ? AND fecha < ?
            ""
    movimientos = consultaSQL(query , [desde,hasta])
else:
    query = ""
            SELECT * FROM movimientos WHERE fecha > ? AND fecha < ? AND concepto LIKE "%?%"
            ""
    movimientos = consultaSQL(query , [desde,hasta,texto])
"""

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
    form = MovimientosForm()
    if request.method == "GET":
        filas = consultaSQL("SELECT * FROM movimientos WHERE id= ?", [id])
        if len(filas) == 0:
            flash("No se encuentra el movimiento.", "alert")
            return render_template('modificar.html', form = None)
    else:
        #Si se pulsa el botón aceptar
        if form.submit.data:
            #Si los archivos están validados.
            if form.validate():
                query = """
                        UPDATE movimientos SET fecha=?, concepto=?, categoria=?,esGasto=?, cantidad=? WHERE id=? 
                        """
                try:
                    modificaSQL(query, [form.fecha.data,
                                        form.concepto.data,
                                        form.categoria.data,
                                        form.esGasto.data,
                                        form.cantidad.data,
                                        id])
                except sqlite3.error as e:
                    flash("Se ha producido un error de base de datos, vuelva a intentarlo", 'error')
                    print("Error en update", e) # < Esta línea es para el operador, indica el error en consola para el programador.
                    return redirect(url_for('index'))
                    
                flash("Modificación realizada con éxito", 'mensaje')    
                return redirect(url_for('index'))
            #Si los archivos NO están validados
            else:
                return render_template('modificar.html', form = form)
        #Si se pulsa el boton cancelar
        elif form.Nosubmit.data:
            flash("Modificación Anulada", 'mensaje')    
            return render_template('modificar.html', form = form, id = id)

    registro = filas[0]
    registro["fecha"] = date.fromisoformat(registro["fecha"])
    form = MovimientosForm(data = registro)
    return render_template('modificar.html', form = form, id = id)


    

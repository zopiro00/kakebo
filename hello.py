from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hola Mundo"

@app.route("/adios")
def bye():
    return "Hasta luego, cocodrilo"
from flask import Flask, render_template, url_for, request, redirect, session, flash
import cx_Oracle
app = Flask(__name__)
app.config["SECRET_KEY"] = '4495d60fb193c77b54e891a4fe200e7e'

@app.route("/", methods=["POST","GET"]) #vista de la página principal - registro
def inicio():
    if "usuario" in session:
        return redirect(url_for("paises"))
    else:
        return render_template("inicio.html")

@app.route("/Inicio_Sesion")
def inicio_sesion():
    return render_template("inicio_sesion.html")

@app.route("/Registro")
def registro():
    return render_template("registro.html")

@app.route("/Avion")
def avion():
    return render_template("avion.html")

@app.route("/Boleta")
def boleta():
    return render_template("boleta.html")

@app.route("/Cliente")
def cliente():
    return render_template("cliente.html")

@app.route("/Compañia")
def compañia():
    return render_template("compañia.html")

@app.route("/Detalle_Compra")
def detalle_compra():
    return render_template("detalle_compra.html")

@app.route("/Encuesta")
def encuesta():
    return render_template("encuesta.html")

@app.route("/Forma_Pago")
def forma_pago():
    return render_template("forma_pago.html")

@app.route("/Vuelo")
def vuelo():
    return render_template("vuelo.html")

@app.route("/Debito")
def debito():
    return render_template("debito.html")

@app.route("/Credito")
def credito():
    return render_template("credito.html")

@app.route("/Pasaje")
def pasaje():
    return render_template("pasaje.html")

@app.route("/Itinerario")
def itinerario():
    return render_template("itinerario.html")

@app.route("/Origen")
def origen():
    return render_template("oreigen.html")

@app.route("/Destino")
def destino():
    return render_template("destino.html")

@app.route("/Pasajero")
def pasajero():
    return render_template("pasajero.html")

@app.route("/Aeropuerto")
def aeropuerto():
    return render_template("aeropuerto.html")

@app.route("/Ciudad")
def ciudad():
    return render_template("ciudad.html")

@app.route("/Pais", methods=["GET"]) #Vista de los Paises
def pais():
    return render_template("pais.html")

def conectar_bdd():
    try:    
        servidor = cx_Oracle.makedsn('localhost', '1521', service_name='xe') 
        conexion = cx_Oracle.connect(user='AVIONES', password='AVIONES', dsn = servidor) 
        return conexion
    except cx_Oracle.DatabaseError as e:
        error = e.args[0]
        return False

if __name__ == "__main__":
    app.run(debug=True)
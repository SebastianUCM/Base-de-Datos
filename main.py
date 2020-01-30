from flask import Flask, render_template, url_for, request, redirect, session, flash
import cx_Oracle
app = Flask(__name__)
app.config["SECRET_KEY"] = '4495d60fb193c77b54e891a4fe200e7e'

@app.route("/", methods=["POST","GET"]) #vista de la página principal - registro
def inicio():
    if "CLIENTE" in session:
        print("TIPO DE USUARIO: ",session["TIPO"]) #TIPO DE USUARIO
        return render_template("inicio.html")
    else:
        print("TIPO DE USUARIO: VISITANTE") #TIPO DE USUARIO
        return render_template("inicio.html")

@app.route("/inicio_Sesion", methods=["POST","GET"]) #vista inicio sesion
def inicio_sesion():
    if request.method == "POST":
        CLIENTE = dict()
        CLIENTE["EMAIL"] = request.form['email_usuario']
        CLIENTE["CONTRASENA"] = request.form['contrasena_usuario']
        conexion = conectar_bdd("AVIONES_CLIENTE","123")
        if conexion != False:
            sentencia = conexion.cursor()
            resultado = sentencia.var(cx_Oracle.STRING) 
            mensaje = sentencia.var(cx_Oracle.STRING)
            TIPO = sentencia.var(cx_Oracle.STRING)
            sentencia.callproc("AVIONES.INICIAR_SESION",(CLIENTE["EMAIL"], CLIENTE["CONTRASENA"], resultado, mensaje, TIPO))
            sentencia.close()
            if resultado.getvalue() == "TRUE":
                session["CLIENTE"] = CLIENTE["EMAIL"]
                session["TIPO"] = TIPO.getvalue()
                print("USUARIO INICIADO :",session["CLIENTE"])
                print("TIPO DE USUARIO :",session["TIPO"]) #TIPO DE USUARIO
                flash(mensaje.getvalue(), "success")
            else:
                flash(mensaje.getvalue(), "danger")
        else:
            flash("No se pudo realizar la conexion", "danger")
        return redirect(url_for("inicio_sesion"))
    else:
        return render_template("inicio_sesion.html")

@app.route("/Registro", methods=["POST","GET"])
def registro():
    if request.method == "POST":
        CLIENTE = dict()
        CLIENTE["NOMBRE"] = request.form["nombre_usuario"]
        CLIENTE["APELLIDO"] = request.form["apellido_usuario"]
        CLIENTE["EMAIL"] = request.form["email_usuario"]
        CLIENTE["CONTRASENA"] = request.form["contrasena_usuario"]
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            resultado = sentencia.var(cx_Oracle.STRING) 
            mensaje = sentencia.var(cx_Oracle.STRING)
            sentencia.callproc("INGRESAR_CLIENTE_REGISTRO",(CLIENTE["NOMBRE"], CLIENTE["APELLIDO"], CLIENTE["EMAIL"], CLIENTE["CONTRASENA"], resultado, mensaje))
            sentencia.close()
            if resultado.getvalue() == "TRUE":
                flash(mensaje.getvalue(), "success")
            else:
                flash(mensaje.getvalue(), "danger")
        else:
            flash("No se pudo realizar la conexion", "danger")
        return render_template("registro.html")
    else:  
        return render_template("registro.html")

@app.route("/Perfil", methods=["POST","GET"]) # Vista Perfil
def perfil():
    if request.method == "POST":
        CLIENTE = dict()
        CLIENTE["NOMBRE"] = request.form['nombre_usuario']
        CLIENTE["APELLIDO"] = request.form['apellido_usuario']
        CLIENTE["FECHA_NACIMIENTO"] = request.form['f_na_usuario']
        CLIENTE["GENERO"] = request.form['genero_usuario']
        CLIENTE["TIPO_DOCUMENTO"] = request.form['t_doc_usuario']
        CLIENTE["FECHA_VENCIMIENTO_DOCUMENTO"] = request.form['f_v_doc__usuario']
        CLIENTE["NUMERO_DOCUMENTO"] = request.form['n_doc_usuario']
        CLIENTE["NACIONALIDAD"] = request.form['nacionalidad_usuario']
        CLIENTE["PAIS"] = request.form['pais_usuario']
        CLIENTE["TELEFONO"] = request.form['telefono_usuario']
        CLIENTE["EMAIL"] = request.form['email_usuario']
        CLIENTE["CONTRASENA"] = request.form['contrasena_usuario']
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            resultado = sentencia.var(cx_Oracle.STRING) 
            mensaje = sentencia.var(cx_Oracle.STRING)
            TIPO = sentencia.var(cx_Oracle.STRING)
            sentencia.callproc("AVIONES.ACTUALIZA_CLIENTE",(CLIENTE["NOMBRE"], CLIENTE["APELLIDO"], CLIENTE["FECHA_NACIMIENTO"], CLIENTE["GENERO"], CLIENTE["TIPO_DOCUMENTO"], CLIENTE["FECHA_VENCIMIENTO_DOCUMENTO"], CLIENTE["NUMERO_DOCUMENTO"], CLIENTE["NACIONALIDAD"], CLIENTE["PAIS"], CLIENTE["TELEFONO"], CLIENTE["EMAIL"], CLIENTE["CONTRASENA"], resultado, mensaje))
            sentencia.close()
            if resultado.getvalue() == "TRUE":
                session["CLIENTE"] = CLIENTE["EMAIL"]
                session["TIPO"] = TIPO.getvalue()
                print(session["CLIENTE"])
                print(session["TIPO"])
                flash(mensaje.getvalue(), "success")
            else:
                flash(mensaje.getvalue(), "danger")
        else:
            flash("No se pudo realizar la conexion", "danger")
        return redirect(url_for("perfil"))
    else:
        return render_template("perfil.html")

@app.route('/Administra_Itinerario', methods=['POST','GET'])
def administra_itinerario():
    if request.method == "GET":
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT * FROM ITINERARIO")
            sentencia.execute(None)
            itinerarios = []
            for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                itinerarios.append(fila)      #Imprimimos cada fila
            sentencia.close()  #Cerramos la conexión
            return render_template("administra_itinerario.html", itinerarios = itinerarios)
        else:
            flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("administra_itinerario"))
    else:
        return render_template("administra_itinerario.html")

@app.route("/Administra_Vuelo", methods=["POST","GET"])
def administra_vuelo():
    return render_template('administra_vuelo.html')

@app.route("/cerrar_sesion")
def cerrar_sesion():
    if session["CLIENTE"]:
        session.pop("CLIENTE", None)
        session.pop("TIPO", None)
    return redirect(url_for("inicio"))

@app.route("/Cliente")
def cliente():
    if request.method == "GET":
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT ID_CLIENTE, NOMBRE, APELLIDO, TELEFONO, EMAIL, ROL FROM CLIENTE")
            sentencia.execute(None)
            clientes = []
            for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                clientes.append(fila)      #Imprimimos cada fila
            sentencia.close()  #Cerramos la conexión
            return render_template("cliente.html", clientes = clientes)
        else:
            flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("cliente"))
    else:
        return render_template("cliente.html")

@app.route("/modifica_rol_cliente", methods=["POST","GET"]) #vista modificar producto
def modifica_rol_cliente():
    print(session)
    if "CLIENTE" in session:
        if request.method == "POST":
            conexion = conectar_bdd("AVIONES","AVIONES")
            codigo = request.form["modifica_rol_cliente"]
            print("El Id del Cliente es: ",codigo)
            email_usuario = session["CLIENTE"]
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT ID_CLIENTE, NOMBRE, APELLIDO, TELEFONO, EMAIL, ROL FROM CLIENTE WHERE ID_CLIENTE = :codigo")
            sentencia.execute(None, {'codigo': codigo})
            cliente = None
            for fila in sentencia:
                cliente = fila
            return render_template("modifica_rol_cliente.html", cliente = cliente)
        else:
            return render_template("modifica_rol_cliente.html")
    else:
        return redirect(url_for("cliente"))

@app.route("/guardar_modificar_cliente", methods=["POST","GET"]) #vista modificar producto
def guardar_modificar_cliente():
    if "CLIENTE" in session:
        if request.method == "POST":
            CLIENTE = dict()
            CLIENTE["ID_CLIENTE"] = request.form["id_cliente"]
            CLIENTE["NOMBRE"] = request.form["nombre_cliente"]
            CLIENTE["APELLIDO"] = request.form["apellido_cliente"]
            CLIENTE["TELEFONO"] = request.form["telefono_cliente"]
            CLIENTE["EMAIL"] = request.form["email_cliente"]
            CLIENTE["ROL"] = request.form["rol_cliente"]
            email_usuario = session["CLIENTE"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                email_usuario = session["CLIENTE"]
                sentencia.callproc("MODIFICAR_ROL_CLIENTE", (CLIENTE["ID_CLIENTE"],CLIENTE["NOMBRE"],CLIENTE["APELLIDO"],CLIENTE["TELEFONO"],CLIENTE["EMAIL"],CLIENTE["ROL"], resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("cliente"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("cliente"))
        else:
            return redirect({url_for("cliente")})
    else:
        return redirect(url_for("inicio_sesion"))

@app.route("/eliminar_cliente", methods=["POST","GET"]) #vista modificar CLIENTE
def eliminar_cliente():
    if "usuario" in session:
        if request.method == "POST":
            codigo = request.form["eliminar_cliente"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                email_cliente = session["CLIENTE"]
                sentencia.callproc("ELIMINAR_CLIENTE", (codigo,email_cliente, resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("cliente"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("cliente"))
        else:
            return redirect(url_for("cliente"))
    else:
        return redirect(url_for("cliente"))

@app.route("/Aeropuerto")
def aeropuerto():
    if request.method == "GET":
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT ID_AEROPUERTO, DIRECCION, CIUDAD, NOMBRE FROM AEROPUERTO")
            sentencia.execute(None)
            aeropuertos = []
            for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                aeropuertos.append(fila)      #Imprimimos cada fila
            sentencia.close()  #Cerramos la conexión
            return render_template("aeropuerto.html", aeropuertos = aeropuertos)
        else:
            flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("aeropuerto"))
    else:
        return render_template("aeropuerto.html")

@app.route("/Insertar_Aeropuerto", methods=["POST","GET"]) #vista insertar Aeropuerto
def insertar_aerpuerto():
    if "CLIENTE" in session:
        if request.method == "POST":
            AEROPUERTO = dict()
            AEROPUERTO["ID_AEROPUERTO"] = request.form["cod_aeropuerto"]
            AEROPUERTO["DIRECCION"] = request.form["direccion_aeropuerto"]
            AEROPUERTO["CIUDAD"] = request.form["ciudad_aeropuerto"]
            AEROPUERTO["NOMBRE"] = request.form["nombre_aeropuerto"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                rut_usuario = session["usuario"]
                sentencia.callproc("INGRESAR_AEROPUERTO", (AEROPUERTO["ID_AEROPUERTO"],AEROPUERTO["DIRECCION"],AEROPUERTO["CIUDAD"],AEROPUERTO["NOMBRE"], resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("insertar_aerpuerto"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("aeropuerto"))
        else:
            conexion = conectar_bdd("AVIONES","AVIONES")
            sentencia = conexion.cursor()
            sentencia.execute("SELECT * FROM CIUDAD")
            ciudades = []
            for fila in sentencia:
                ciudades.append(fila)
            sentencia.close()
            return render_template("insertar_aerpuerto.html", ciudades = ciudades)
    else:
        return redirect(url_for("aeropuerto"))

@app.route("/Insertar_Itinerario", methods=["POST","GET"]) #vista insertar Aeropuerto
def insertar_itinerario():
    if "CLIENTE" in session:
        if request.method == "POST":
            ITINERARIO = dict()
            ITINERARIO["ID_ITINERARIO"] = request.form["id_itinerario_a"]
            ITINERARIO["HORA_LLEGADA"] = request.form["hora_llegada_a"]
            ITINERARIO["HORA_SALIDA"] = request.form["hora_salida_a"]
            ITINERARIO["FECHA_LLEGADA"] = request.form["fecha_llegada_a"]
            ITINERARIO["FECHA_SALIDA"] = request.form["fecha_salida_a"]
            ITINERARIO["ORIGEN"] = request.form["origen_a"]
            ITINERARIO["DESTINO"] = request.form["destino_a"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                rut_usuario = session["usuario"]
                sentencia.callproc("INGRESAR_ITINERARIO", (ITINERARIO["ID_ITINERARIO"],ITINERARIO["HORA_LLEGADA"],ITINERARIO["HORA_SALIDA"],ITINERARIO["FECHA_LLEGADA"],ITINERARIO["ORIGEN"],ITINERARIO["DESTINO"], resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("insertar_itinerario"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("administra_itinerario"))
        else:
            conexion = conectar_bdd("AVIONES","AVIONES")
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT O.ID_ORIGEN, O.AEROPUERTO, A.NOMBRE, C.NOMBRE, P.NOMBRE FROM AEROPUERTO A, CIUDAD C,PAIS P, ORIGEN O WHERE O.AEROPUERTO = A.ID_AEROPUERTO AND P.ID_PAIS = C.PAIS AND C.ID_CIUDAD = A.CIUDAD") 
            ciudades_o = []
            for elem in sentencia:
                ciudades_o.append(elem)
            sentencia.close()
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT D.ID_DESTINO, D.AEROPUERTO, A.NOMBRE, C.NOMBRE, P.NOMBRE FROM AEROPUERTO A, CIUDAD C,PAIS P, DESTINO D WHERE D.AEROPUERTO = A.ID_AEROPUERTO AND P.ID_PAIS = C.PAIS AND C.ID_CIUDAD = A.CIUDAD")
            ciudades_d = []
            for fila in sentencia:
                ciudades_d.append(fila)
            sentencia.close()            
            return render_template("insertar_itinerario.html", ciudades_o = ciudades_o, ciudades_d = ciudades_d)
    else:
        return redirect(url_for("administra_itinerario"))

@app.route("/modificar_aeropuerto", methods=["POST","GET"]) #vista modificar Aeropuerto
def modificar_aeropuerto():
    if "CLIENTE" in session:
        if request.method == "POST":
            conexion = conectar_bdd("AVIONES","AVIONES")
            codigo = request.form["modificar_aeropuerto"]
            print(codigo)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT ID_AEROPUERTO,DIRECCION,CIUDAD,NOMBRE FROM AEROPUERTO WHERE ID_AEROPUERTO = :codigo")
            sentencia.execute(None, {'codigo': codigo})
            aeropuerto = None
            for fila in sentencia:
                aeropuerto = fila
            return render_template("modificar_aeropuerto.html", aeropuerto = aeropuerto)
        else:
            return render_template("modificar_aeropuerto.html")
    else:
        return redirect(url_for("aeropuerto"))

@app.route("/guardar_modificar_aeropuerto", methods=["POST","GET"]) #vista modificar producto
def guardar_modificar_aeropuerto():
    if "CLIENTE" in session:
        if request.method == "POST":
            AEROPUERTO = dict()
            AEROPUERTO["ID_AEROPUERTO"] = request.form["cod_aeropuerto"]
            AEROPUERTO["DIRECCION"] = request.form["direccion_aeropuerto"]
            AEROPUERTO["CIUDAD"] = request.form["ciudad_aeropuerto"]
            AEROPUERTO["NOMBRE"] = request.form["nombre_aeropuerto"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("ACTUALIZAR_AEROPUERTO", (AEROPUERTO["ID_AEROPUERTO"],AEROPUERTO["DIRECCION"],AEROPUERTO["CIUDAD"],AEROPUERTO["NOMBRE"], resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("aeropuerto"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("aeropuerto"))
        else:
            return redirect({url_for("aeropuerto")})
    else:
        return redirect(url_for("inicio_sesion"))

@app.route("/eliminar_aeropuerto", methods=["POST","GET"]) #vista modificar AEROPUERTO
def eliminar_aeropuerto():
    if "CLIENTE" in session:
        if request.method == "POST":
            codigo = request.form["eliminar_aeropuerto"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("BORRAR_AEROPUERTO", (codigo, resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("aeropuerto"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("aeropuerto"))
        else:
            return redirect(url_for("aeropuerto"))
    else:
        return redirect(url_for("aeropuerto"))

@app.route("/Origen")
def origen():
    if request.method == "GET":
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT O.ID_ORIGEN, O.AEROPUERTO, A.NOMBRE, C.NOMBRE, P.NOMBRE FROM AEROPUERTO A, CIUDAD C,PAIS P, ORIGEN O WHERE O.AEROPUERTO = A.ID_AEROPUERTO AND P.ID_PAIS = C.PAIS AND C.ID_CIUDAD = A.CIUDAD")
            sentencia.execute(None)
            origenes = []
            for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                origenes.append(fila)      #Imprimimos cada fila
            sentencia.close()  #Cerramos la conexión
            return render_template("origen.html", origenes = origenes)
        else:
            flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("origen"))
    else:
        return render_template("origen.html")
    return render_template("origen.html")

@app.route("/Destino")
def destino():
    if request.method == "GET":
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT D.ID_DESTINO, D.AEROPUERTO, A.NOMBRE, C.NOMBRE, P.NOMBRE FROM AEROPUERTO A, CIUDAD C,PAIS P, DESTINO D WHERE D.AEROPUERTO = A.ID_AEROPUERTO AND P.ID_PAIS = C.PAIS AND C.ID_CIUDAD = A.CIUDAD")
            sentencia.execute(None)
            destinos = []
            for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                destinos.append(fila)      #Imprimimos cada fila
            sentencia.close()  #Cerramos la conexión
            return render_template("destino.html", destinos = destinos)
        else:
            flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("destino"))
    else:
        return render_template("destino.html")    
    return render_template("destino.html")












@app.route("/Avion")
def avion():
    return render_template("avion.html")

@app.route("/Boleta")
def boleta():
    return render_template("boleta.html")

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



@app.route("/Pasajero")
def pasajero():
    return render_template("pasajero.html")



@app.route("/Ciudad")
def ciudad():
    return render_template("ciudad.html")

#@app.route("/Pais", methods=["GET"]) #Vista de los Paises
#def pais():
#    return render_template("pais.html")


@app.route("/Pais", methods=["GET"]) #vista de los productos
def pais():
    if "CLIENTE" in session:
        email_usuario = session["CLIENTE"]
        conexion = conectar_bdd()
        if conexion != False:
            sentencia = conexion.cursor()
            sentencia.execute("SELECT * FROM pais")
            #sentencia.execute(None, {'EMAIL': email_usuario})
            pais = []
            for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                pais.append(fila)      #Imprimimos cada fila
                sentencia.close()  #Cerramos la conexión
            return render_template("pais.html")
        else:
            flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("pais"))
    else:
        return redirect(url_for("pais"))

def conectar_bdd(user,passw):
    try:    
        servidor = cx_Oracle.makedsn('localhost', '1521', service_name='xe') 
        conexion = cx_Oracle.connect(user, passw, dsn = servidor) 
        return conexion
    except cx_Oracle.DatabaseError as e:
        error = e.args[0]
        print(error)
        return False

if __name__ == "__main__":
    app.run(debug=True)
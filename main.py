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
            sentencia.callproc("ACTUALIZA_CLIENTE",(CLIENTE["NOMBRE"], CLIENTE["APELLIDO"], CLIENTE["FECHA_NACIMIENTO"], CLIENTE["GENERO"], CLIENTE["TIPO_DOCUMENTO"], CLIENTE["FECHA_VENCIMIENTO_DOCUMENTO"], CLIENTE["NUMERO_DOCUMENTO"], CLIENTE["NACIONALIDAD"], CLIENTE["PAIS"], CLIENTE["TELEFONO"], CLIENTE["EMAIL"], CLIENTE["CONTRASENA"], resultado, mensaje))
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
                sentencia.callproc("INGRESAR_ITINERARIO", (ITINERARIO["ID_ITINERARIO"],ITINERARIO["HORA_LLEGADA"],ITINERARIO["HORA_SALIDA"],ITINERARIO["FECHA_LLEGADA"],ITINERARIO["FECHA_SALIDA"],ITINERARIO["ORIGEN"],ITINERARIO["DESTINO"], resultado, mensaje))
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
            sentencia_1 = conexion.cursor()
            sentencia.prepare("SELECT ID_DESTINO FROM DESTINO ")
            sentencia.execute(None)
            destinos = []
            sentencia_1.prepare("SELECT ID_ORIGEN FROM ORIGEN")
            sentencia_1.execute(None)
            origenes = []
            for fila in sentencia:
                destinos.append(fila)
            sentencia.close()
            for elem in sentencia_1:
                origenes.append(elem)
            sentencia_1.close()
            return render_template("insertar_itinerario.html", destinos = destinos, origenes=origenes)
    else:
        return redirect(url_for("insertar_itinerario"))

@app.route("/eliminar_itinerario", methods=["POST","GET"]) #vista modificar itinerario
def eliminar_itinerario():
    if "CLIENTE" in session:
        if request.method == "POST":
            codigo = request.form["eliminar_itinerario"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("BORRAR_ITINERARIO", (codigo, resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("administra_itinerario"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("administra_itinerario"))
        else:
            return redirect(url_for("administra_itinerario"))
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

@app.route("/ciudad",methods=["POST","GET"]) #vista de los productos
def ciudad():
        if request.method == "GET":
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                sentencia.prepare("SELECT ID_CIUDAD,NOMBRE,PAIS FROM CIUDAD")
                sentencia.execute(None)
                ciudades = []
                for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                    ciudades.append(fila)      #Imprimimos cada fila
                sentencia.close()  #Cerramos la conexión
                return render_template("ciudad.html", ciudades = ciudades)
            else:
                flash("No se pudo realizar la conexion", "danger")
                return redirect(url_for("ciudad"))
        else:
            return render_template("ciudad.html")

@app.route('/insertar_ciudad', methods=['POST','GET'])
def insertar_ciudad():
    if request.method == 'POST':
        CIUDAD= dict()
        CIUDAD['ID_CIUDAD'] = request.form['codigo_ciudad']
        CIUDAD['NOMBRE'] = request.form['nombre_ciudad']
        CIUDAD['PAIS'] = request.form['id_pais']
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            resultado = sentencia.var(cx_Oracle.STRING)
            mensaje = sentencia.var(cx_Oracle.STRING)
            sentencia.callproc('INSERTAR_CIUDAD',(CIUDAD['ID_CIUDAD'],CIUDAD['NOMBRE'],CIUDAD['PAIS'],resultado,mensaje))
            sentencia.close()
            if resultado.getvalue() == 'TRUE':
                flash(mensaje.getvalue(),'success')
            else:
                flash(mensaje.getvalue(),'danger')
                return redirect(url_for("insertar_ciudad"))
        else:
            flash('No fue posible conectarse a la base de datos','danger')
        return redirect(url_for('insertar_ciudad'))
    else:
            conexion = conectar_bdd("AVIONES","AVIONES")
            sentencia = conexion.cursor()
            sentencia.execute("SELECT ID_PAIS FROM PAIS")
            paises = []
            for fila in sentencia:
                paises.append(fila)
            sentencia.close()
            return render_template("insertar_ciudad.html", paises = paises)

@app.route("/actualizar_ciudad", methods=["POST","GET"]) 
def actualizar_ciudad():
    if request.method == "POST":
        CIUDAD= dict()
        CIUDAD['ID_CIUDAD'] = request.form['codigo_ciudad']
        CIUDAD['NOMBRE'] = request.form['nombre_ciudad']
        CIUDAD['PAIS'] = request.form['id_pais']
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            resultado = sentencia.var(cx_Oracle.STRING) 
            mensaje = sentencia.var(cx_Oracle.STRING)
            TIPO = sentencia.var(cx_Oracle.STRING)
            sentencia.callproc("ACTUALIZAR_CIUDAD",(CIUDAD['ID_CIUDAD'],CIUDAD['NOMBRE'],CIUDAD['PAIS'],resultado,mensaje))
            sentencia.close()
            if resultado.getvalue() == 'TRUE':
                flash(mensaje.getvalue(),'success')
            else:
                flash(mensaje.getvalue(),'danger')
        else:
            flash("No se pudo realizar la conexion", "danger")
        return redirect(url_for("actualizar_ciudad"))
    else:
            conexion = conectar_bdd("AVIONES","AVIONES")
            sentencia = conexion.cursor()
            sentencia.execute("SELECT ID_PAIS FROM PAIS")
            paises = []
            for fila in sentencia:
                paises.append(fila)
            sentencia.close()
            return render_template("actualizar_ciudad.html", paises = paises)

@app.route("/eliminar_ciudad", methods=["POST","GET"]) #vista modificar CLIENTE
def eliminar_ciudad():
        if request.method == "POST":
            ID_CIUDAD = request.form["eliminar_ciudad"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("BORRAR_CIUDAD", (ID_CIUDAD,resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("ciudad"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("ciudad"))
        else:
            return redirect(url_for("ciudad"))

@app.route("/mostrar_pais")
def mostrar_paises():
        if request.method == "GET":
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                sentencia.prepare("SELECT ID_PAIS,NOMBRE FROM PAIS")
                sentencia.execute(None)
                paises = []
                for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                    paises.append(fila)      #Imprimimos cada fila
                sentencia.close()  #Cerramos la conexión
                return render_template("mostrar_paises.html", paises = paises)
            else:
                flash("No se pudo realizar la conexion", "danger")
                return redirect(url_for("mostrar_paises"))
        else:
            return render_template("mostrar_paises.html")

@app.route('/ingresar_pais', methods=['POST','GET'])
def ingresar_pais():
    if request.method == 'POST':
        PAIS= dict()
        PAIS['ID_PAIS'] = request.form['id']
        PAIS['NOMBRE'] = request.form['nombre_p']
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            resultado = sentencia.var(cx_Oracle.STRING)
            mensaje = sentencia.var(cx_Oracle.STRING)
            sentencia.callproc('INSERTAR_PAIS',(PAIS['ID_PAIS'],PAIS['NOMBRE'],resultado,mensaje))
            sentencia.close()
            if resultado.getvalue() == 'TRUE':
                flash(mensaje.getvalue(),'success')
            else:
                flash(mensaje.getvalue(),'danger')
        else:
            flash('No fue posible conectarse a la base de datos','danger')
        return redirect(url_for('ingresar_pais'))
    else:
        return render_template('ingresar_pais.html')

@app.route("/actualizar_pais", methods=["POST","GET"]) 
def actualizar_pais():
    if request.method == "POST":
        PAIS = dict()
        PAIS['ID_PAIS'] = request.form['id']
        PAIS['NOMBRE'] = request.form['nombre_p']
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            resultado = sentencia.var(cx_Oracle.STRING) 
            mensaje = sentencia.var(cx_Oracle.STRING)
            TIPO = sentencia.var(cx_Oracle.STRING)
            sentencia.callproc("ACTUALIZAR_PAIS",(PAIS['ID_PAIS'],PAIS['NOMBRE'],resultado,mensaje))
            sentencia.close()
            if resultado.getvalue() == 'TRUE':
                flash(mensaje.getvalue(),'success')
            else:
                flash(mensaje.getvalue(),'danger')
        else:
            flash("No se pudo realizar la conexion", "danger")
        return redirect(url_for("actualizar_pais"))
    else:
        return render_template("actualizar_pais.html")

@app.route("/eliminar_pais", methods=["POST","GET"]) #vista modificar CLIENTE
def eliminar_pais():
        if request.method == "POST":
            ID_PAIS = request.form["eliminar_pais"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("BORRAR_PAIS", (ID_PAIS,resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("mostrar_paises"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("mostrar_paises"))
        else:
            return redirect(url_for("mostrar_paises"))

@app.route("/avion", methods=["POST","GET"]) #vista de los productos
def avion():
    if request.method == "GET":
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT ID_AVION,MODELO,CAPACIDAD,ANIO FROM AVION")
            sentencia.execute(None)
            aviones = []
            for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                aviones.append(fila)      #Imprimimos cada fila
            sentencia.close()  #Cerramos la conexión
            return render_template("avion.html", aviones = aviones)
        else:
            flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("avion"))
    else:
        return render_template("avion.html")

@app.route("/Insertar_Avion", methods=["POST","GET"]) #vista insertar Aeropuerto
def insertar_avion():
    if "CLIENTE" in session:
        if request.method == "POST":
            AVION = dict()
            AVION["ID_AVION"] = request.form["cod_avion"]
            AVION["MODELO"] = request.form["modelo"]
            AVION["CAPACIDAD"] = request.form["capacidad"]
            AVION["ANIO"] = request.form["ano"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("INGRESAR_AVION", (AVION["ID_AVION"],AVION["MODELO"],AVION["CAPACIDAD"],AVION["ANIO"], resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("insertar_avion"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("avion"))
        else:
            return render_template("insertar_avion.html")
    else:
        return redirect(url_for("avion"))

@app.route("/modificar_avion", methods=["POST","GET"]) #vista modificar Aeropuerto
def modificar_avion():
    if "CLIENTE" in session:
        if request.method == "POST":
            conexion = conectar_bdd("AVIONES","AVIONES")
            codigo = request.form["modificar_avion"]
            print(codigo)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT ID_AVION,MODELO,CAPACIDAD,ANIO FROM AVION WHERE ID_AVION = :codigo")
            sentencia.execute(None, {'codigo': codigo})
            avion = None
            for fila in sentencia:
                avion = fila
            return render_template("modificar_avion.html", avion = avion)
        else:
            return render_template("modificar_avion.html")
    else:
        return redirect(url_for("avion"))

@app.route("/guardar_modificar_avion", methods=["POST","GET"]) #vista modificar producto
def guardar_modificar_avion():
    if "CLIENTE" in session:
        if request.method == "POST":
            AVION = dict()
            AVION["ID_AVION"] = request.form["cod_avion"]
            AVION["MODELO"] = request.form["modelo"]
            AVION["CAPACIDAD"] = request.form["capacidad"]
            AVION["ANIO"] = request.form["ano"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("ACTUALIZAR_AVION", (AVION["ID_AVION"],AVION["MODELO"],AVION["CAPACIDAD"],AVION["ANIO"], resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("avion"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("avion"))
        else:
            return redirect({url_for("avion")})
    else:
        return redirect(url_for("inicio_sesion"))

@app.route("/eliminar_avion", methods=["POST","GET"]) #vista modificar AEROPUERTO
def eliminar_avion():
    if "CLIENTE" in session:
        if request.method == "POST":
            ID_AVION = request.form["eliminar_avion"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("BORRAR_AVION", (ID_AVION, resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("avion"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("avion"))
        else:
            return redirect(url_for("avion"))
    else:
        return redirect(url_for("avion"))

@app.route("/Vuelo", methods=["POST","GET"])#vista de los productos
def vuelo():
    if request.method == "GET":
        conexion = conectar_bdd("AVIONES","AVIONES")
        if conexion != False:
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT * FROM VUELO")
            sentencia.execute(None)
            vuelos = []
            for fila in sentencia: #Para ver cada fila, hay que recorrer la lista una por una
                vuelos.append(fila)      #Imprimimos cada fila
            sentencia.close()  #Cerramos la conexión
            return render_template("vuelo.html", vuelos = vuelos)
        else:
            flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("vuelo"))
    else:
        return render_template("vuelo.html")

@app.route("/insertar_vuelo", methods=["POST","GET"]) #vista insertar producto
def insertar_vuelo():
    if "CLIENTE" in session:
        if request.method == "POST":
            VUELO = dict()
            VUELO["ID_VUELO"] = request.form["ins_id_vuelo"]
            VUELO["CAPACIDAD"] = request.form["ins_capacidad"]
            VUELO["AVION"] = request.form["ins_avion"]
            VUELO["ITINERARIO"] = request.form["ins_itinerario"]
            VUELO["VALOR"] = request.form["valor_vuelo"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("INSERTAR_VUELO", (VUELO["ID_VUELO"],VUELO["CAPACIDAD"],VUELO["AVION"], VUELO["ITINERARIO"],VUELO["VALOR"],resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("insertar_vuelo"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("vuelo"))
        else:
            conexion = conectar_bdd("AVIONES","AVIONES")
            sentencia = conexion.cursor()
            sentencia_1 = conexion.cursor()
            sentencia.prepare("SELECT * FROM AVION ")
            sentencia.execute(None)
            aviones= []
            sentencia_1.prepare("SELECT * FROM ITINERARIO")
            sentencia_1.execute(None)
            itinerarios = []
            for fila in sentencia:
                aviones.append(fila)
            sentencia.close()
            for elem in sentencia_1:
                itinerarios.append(elem)
            sentencia_1.close()
            return render_template("insertar_vuelo.html", aviones = aviones, itinerarios=itinerarios)
    else:
        return redirect(url_for("vuelo"))


@app.route("/modificar_vuelo", methods=["POST","GET"]) #vista modificar Aeropuerto
def modificar_vuelo():
    if "CLIENTE" in session:
        if request.method == "POST":
            conexion = conectar_bdd("AVIONES","AVIONES")
            codigo = request.form["modificar_vuelo"]
            print(codigo)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            sentencia = conexion.cursor()
            sentencia.prepare("SELECT ID_VUELO, CAPACIDAD,AVION,ITINERARIO,VALOR FROM VUELO WHERE ID_VUELO = :codigo")
            sentencia.execute(None, {'codigo': codigo})
            vuelos = None
            for fila in sentencia:
                vuelos= fila
            return render_template("modificar_vuelo.html", vuelos = vuelos)
        else:
            return render_template("modificar_vuelo.html")
    else:
        return redirect(url_for("vuelo"))

@app.route("/guardar_modificar_vuelo", methods=["POST","GET"]) #vista modificar producto
def guardar_modificar_vuelo():
    if "CLIENTE" in session:
        if request.method == "POST":
            VUELO = dict()
            VUELO["ID_VUELO"] = request.form["id_vuelo"]
            VUELO["CAPACIDAD"] = request.form["capacidad"]
            VUELO["AVION"] = request.form["nombre_avion"]
            VUELO["ITINERARIO"] = request.form["itinerario"]
            VUELO["VALOR"] = request.form["valor_vuelo"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("ACTUALIZAR_VUELO", (VUELO["ID_VUELO"],VUELO["CAPACIDAD"],VUELO["AVION"], VUELO["ITINERARIO"],VUELO["VALOR"],resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("vuelo"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("vuelo"))
        else:
            return redirect({url_for("vuelo")})
    else:
        return redirect(url_for("inicio_sesion"))


@app.route("/eliminar_vuelo", methods=["POST","GET"]) #vista modificar itinerario
def eliminar_vuelo():
    if "CLIENTE" in session:
        if request.method == "POST":
            codigo = request.form["eliminar_vuelo"]
            conexion = conectar_bdd("AVIONES","AVIONES")
            if conexion != False:
                sentencia = conexion.cursor()
                resultado = sentencia.var(cx_Oracle.STRING) 
                mensaje = sentencia.var(cx_Oracle.STRING)
                sentencia.callproc("BORRAR_VUELO", (codigo, resultado, mensaje))
                sentencia.close()
                if resultado.getvalue() == "TRUE":
                    flash(mensaje.getvalue(), "success")
                else:
                    flash(mensaje.getvalue(), "danger")
                    return redirect(url_for("vuelo"))
            else:
                flash("No se pudo realizar la conexion", "danger")
            return redirect(url_for("vuelo"))
        else:
            return redirect(url_for("vuelo"))
    else:
        return redirect(url_for("vuelo"))






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
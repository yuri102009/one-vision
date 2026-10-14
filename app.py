from flask import Flask, render_template,request, redirect, url_for, session, flash
from consultas import consulta, insertar 
from conexion import obtener_conexion
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.secret_key = 'one_vision_clave_secreta' 

#ruta para pagina inicio 
@app.route("/")
def inicio():
     # Llamada a la función para establecer la conexión
    return render_template("inicio.html")

#ruta para pagina de contacto   
@app.route("/contacto", methods=["GET", "POST"])
def contacto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        correo = request.form["correo"]
        asunto = request.form["asunto"]
        mensaje = request.form["mensaje"]

        conexion = obtener_conexion()

        if conexion:
            try:
                cursor = conexion.cursor()

                consulta_sql = "INSERT INTO contacto (nombre, correo, asunto, mensaje) VALUES (%s, %s, %s, %s)" 

                parametros = (nombre, correo, asunto, mensaje)
                cursor.execute(consulta_sql, parametros)

                conexion.commit()

                cursor.close()
                conexion.close()

                return render_template("contacto.html", exito=True)

            except Exception as e:
                print("Error al guardar:", e)
                return render_template("contacto.html", error=True)

        else:
            return render_template("contacto.html", error=True)

    return render_template("contacto.html")

#ruta para pagina de servicios
@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

#ruta para pagina de nosotros
@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

#ruta para pagina de productos
@app.route("/productos")    
def productos():
    return render_template("productos.html")

#ruta para pagina de inicio de sesion
@app.route("/admin/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]

        conexion = obtener_conexion()

        if conexion is None:
            return render_template(
                "login.html",
                error="No se pudo conectar con la base de datos"
            )

        try:

            with conexion.cursor() as cursor:

                sql = "SELECT id, usuario, contraseña FROM administrador WHERE usuario = %s"

                cursor.execute(sql, (usuario,))

                administrador = cursor.fetchone()

            # Comprobar si existe el usuario
            if administrador:

                # Comprobar contraseña
                contraseña_correcta = check_password_hash(
                    administrador["contraseña"],
                    contraseña
                )

                if contraseña_correcta:

                    # Guardar el usuario en la sesión
                    session["admin"] = administrador["id"]
                    session["usuario"] = administrador["usuario"]

                    return redirect("/admin")

                else:

                    return render_template(
                        "login.html",
                        error="Usuario o contraseña incorrectos"
                    )

            else:

                return render_template(
                    "login.html",
                    error="Usuario o contraseña incorrectos"
                )

        finally:

            conexion.close()

    return render_template("login.html")


@app.route("/admin")
def admin():

    # Comprobar si inició sesión
    if "admin" not in session:
        return redirect("/admin/login")

    conexion = obtener_conexion()

    if conexion is None:
        return render_template(
            "admin.html",
            mensajes=[],
            error="No se pudo conectar con la base de datos"
        )

    try:
        with conexion.cursor() as cursor:

            sql = "SELECT nombre, correo, asunto, mensaje FROM contacto ORDER BY id DESC"

            cursor.execute(sql)
            mensajes = cursor.fetchall()

        return render_template(
            "admin.html",
            mensajes=mensajes
        )

    except Exception as e:
        print("Error al consultar los mensajes:", e)

        return render_template(
            "admin.html",
            mensajes=[],
            error="No se pudieron cargar los mensajes"
        )

    finally:
        conexion.close()



@app.route("/admin/mensajes")
def admin_mensajes():

    # Comprobar si inició sesión
    if "admin" not in session:
        return redirect("/admin/login")

    conexion = obtener_conexion()

    if conexion is None:
        return "No se pudo conectar con la base de datos"

    try:
        with conexion.cursor() as cursor:

            sql = "SELECT idmensajes, nombre, correo, asunto, mensaje FROM contacto ORDER BY idmensajes DESC"

            cursor.execute(sql)
            mensajes = cursor.fetchall()

        return render_template(
            "mensajes.html",
            mensajes=mensajes
        )

    except Exception as e:
        print("Error al consultar mensajes:", e)
        return "Ocurrió un error al consultar los mensajes"

    finally:
        conexion.close()




@app.route("/logout")
def logout():

    session.clear()

    return redirect("/admin/login")


if __name__ == "__main__":
    app.run(debug=True)

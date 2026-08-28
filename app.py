from flask import Flask, render_template,  request
from consultas import consulta, insertar 
from conexion import obtener_conexion

app = Flask(__name__)

#ruta para pagina inicio 
@app.route("/")
def inicio():
     # Llamada a la función para establecer la conexión
    return render_template("inicio.html")

#ruta para pagina de contacto   
@app.route("/contacto" , methods=["GET", "POST"])
def contacto():

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        asunto = request.form["asunto"]
        mensaje = request.form["mensaje"]

        # Aquí puedes realizar la inserción en la base de datos utilizando la función insertar
        consulta_sql = "INSERT INTO contacto (nombre, correo, asunto, mensaje) VALUES (%s, %s, %s, %s)"
        parametros = (nombre, correo, asunto, mensaje)
        resultado = insertar(consulta_sql, parametros)

        if resultado == 'Datos insertados correctamente':
            return render_template("contacto.html", exito=True)
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
@app.route("/login")
def login():
    return "aca va la pagina de inicio de sesion"

if __name__ == "__main__":
    app.run(debug=True)
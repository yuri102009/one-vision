from flask import Flask, render_template    

app = Flask(__name__)

#ruta para pagina inicio 
@app.route("/")
def inicio():
    return render_template("inicio.html")

#ruta para pagina de contacto   
@app.route("/contacto")
def contacto():
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
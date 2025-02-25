from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for, flash, g
from datetime import datetime
import forms
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key="contrasenia"
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    print("BEFORER1")
    return None
    
@app.after_request
def after_request(response):
    print("AFTERR1")
    return response

@app.route("/")
def index():
    nom="None"
    titulo="IDGS801"
    lista=["Pedro", "Luis", "Juan"]
    return render_template('index.html', titulo=titulo, nom=nom, lista=lista)

@app.route("/ejemplo1")
def ejemplo1(): 
    return render_template("ejemplo1.html")

@app.route("/ejemplo2")
def ejemplo2():
    return render_template("ejemplo2.html")

@app.route("/operasBas", methods=["GET", "POST"])
def operasBas():
    if request.method == "POST":
        try:
            n1 = int(request.form.get("n1"))
            n2 = int(request.form.get("n2"))
            resultado = n1 * n2
            return render_template("resultado.html", n1=n1, n2=n2, resultado=resultado)
        except ValueError:
            return "Error: Ingresa números válidos"
    return render_template("operasBas.html")

@app.route("/hola")
def hola():
    return "<h1>Ola de mar</h1>"

@app.route("/user/<string:username>")
def user(username):
    return f"<h1>Hola, {username}!</h1>"

@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El número es: {n}!</h1>"

@app.route("/user/<int:user_id>/<string:username>")
def username(user_id, username):
    return f"<h1>Hola, {username}! Tu ID es: {user_id}</h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return f"<h1>La suma es: {n1 + n2}</h1>"

@app.route("/default")
@app.route("/default/<string:param>")
def func(param="Juan"):
    return f"<h1>Hola {param}</h1>"

@app.route("/operas", methods=["GET", "POST"]) 
def operas():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellidos = request.form.get("apellidos")
        return f"<h1>Nombre: {nombre}, Apellidos: {apellidos}</h1>"
    return render_template("operas.html")

# Cinepolis
MAX_BOLETOS = 7
PRECIO_BOLETO = 12
DESCUENTO_TARJETA = 0.1
REGISTRO_COMPRAS = {}
CORTE_TOTAL = 0.0

@app.route("/cinepolis", methods=["GET", "POST"])
def cinepolis():
    global CORTE_TOTAL, REGISTRO_COMPRAS
    resultado = None

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre")
            cantidad_compradores = int(request.form.get("cantidad_compradores"))
            cantidad_boletos = int(request.form.get("cantidad_boletos"))
            tarjeta_cineco = request.form.get("tarjeta_cineco") == "si"

            if cantidad_compradores > MAX_BOLETOS or cantidad_boletos > MAX_BOLETOS:
                raise ValueError("Datos inválidos. Verifica las cantidades.")

            total_compra = cantidad_boletos * PRECIO_BOLETO
            descuento = calcular_descuento(cantidad_boletos, total_compra, tarjeta_cineco)
            total_pagar = total_compra - descuento

            CORTE_TOTAL += total_pagar
            REGISTRO_COMPRAS[nombre] = [cantidad_boletos, total_pagar]

            resultado = {
                "nombre": nombre,
                "cantidad_boletos": cantidad_boletos,
                "tarjeta_cineco": tarjeta_cineco,
                "total": total_pagar
            }

        except ValueError as e:
            resultado = {"error": str(e)}

    return render_template("cinepolis.html", resultado=resultado)

def calcular_descuento(total_boletos, precio_total, usa_tarjeta):
    descuento = 0
    if total_boletos > 5:
        descuento += precio_total * 0.15
    elif 3 <= total_boletos <= 5:
        descuento += precio_total * 0.1
    if usa_tarjeta:
        descuento += (precio_total - descuento) * DESCUENTO_TARJETA
    return descuento

# Signos Zodiacales Chinos
signos = ["Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey",
          "Tigre", "Conejo", "Dragón", "Serpiente", "Caballo", "Cabra"]

@app.route('/zod')
def zod():
    return render_template('signo.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dia, mes, anio = int(request.form['dia']), int(request.form['mes']), int(request.form['anio'])
    sexo = request.form['sexo']

    hoy = datetime.now()
    edad = hoy.year - anio - ((hoy.month, hoy.day) < (mes, dia))
    signo = signos[anio % 12]
    imagen = f"img/{signo.lower()}.jpg"

    return render_template('signo.html', nombre=nombre, apellido=apellido, edad=edad, sexo=sexo, signo=signo, imagen=imagen)

# Alumnos
@app.route("/Alumnos", methods=["GET", "POST"])
def alumnos():
    mat=""
    nom=""
    ape=""
    email=""
    alumno_class=forms.UserForm(request.form)
    if request.method == "POST" and alumno_class.validate():
        mat = alumno_class.matricula.data
        nom = alumno_class.nombre.data
        ape = alumno_class.apellido.data
        email = alumno_class.correo.data
       
        mensaje = 'Bienvenido {}'.format(nom)
        flash(mensaje) 
        
    return render_template("Alumnos.html", form=alumno_class, mat=mat, nom=nom, ape=ape, email=email)


if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True, port=3000)

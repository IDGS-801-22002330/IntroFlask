from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import forms
from flask_wtf.csrf import CSRFProtect
from flask import flash
from flask import g

app = Flask(__name__)
app.secret_key="contrasenia"
csrf=CSRFProtect()



# __________________________ 404 __________________________
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



# __________________________ PRODUCTO VARIO __________________________
@app.route("/")
def index():
    nom='None'
    titulo = "IDGS801"
    lista = ["pedro", "juan", "luis"]
    nom = g.user
    print("Index 2 {}".format(g.user))
    return render_template("index.html", titulo=titulo,nom=nom, lista=lista)

@app.route("/ejemplo1")
def ejemplo1():
    return render_template("ejemplo1.html")

@app.route("/ejemplo2")
def ejemplo2():
    return render_template("ejemplo2.html")

@app.route("/hola")
def hola():
    return "<h1>Hola, mundo---Hola--</h1>"

@app.route("/user/<string:user>")
def user(user):
    return f"<h1>Hello {user}</h1>"

@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El número es: {n}</h1>"

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return f"<h1>Hello {username}, ¡Tu ID es: {id}!</h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return f"<h1>La suma es: {n1 + n2}</h1>"

@app.route("/default/")
@app.route("/default/<string:param>")
def c(param="Juan"):
    return f"<h1>Hola, {param}</h1>"



# __________________________ SIGNO ZODIACAL CHINO __________________________
signos = [
    "Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey",
    "Tigre", "Conejo", "Dragon", "Serpiente", "Caballo", "Cabra"
]

@app.route("/zod", methods=["GET", "POST"])
def zod():
    zod_class = forms.ZodiacoForm(request.form)
    nombre = ""
    apellido = ""
    edad = ""
    signo = ""
    imagen = ""
    sexo = ""
    
    if request.method == "POST" and zod_class.validate():
        nombre = zod_class.nombre.data
        apellido = zod_class.apellido.data
        dia = zod_class.dia.data
        mes = zod_class.mes.data
        anio = zod_class.anio.data
        sexo = zod_class.sexo.data

        hoy = datetime.now()
        edad = hoy.year - anio - ((hoy.month, hoy.day) < (mes, dia))
        signos = [
            "Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey",
            "Tigre", "Conejo", "Dragon", "Serpiente", "Caballo", "Cabra"
        ]
        signo = signos[anio % 12]
        imagen = f"img/{signo.lower()}.jpg"
        
    return render_template('signo.html', form=zod_class, nombre=nombre, apellido=apellido, edad=edad, sexo=sexo, signo=signo, imagen=imagen)



# __________________________ ALUMNOS __________________________
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




# __________________________ CINEPOLIS  __________________________
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



if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True, port=3000)

from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ejemplo1")
def ejemplo1(): 
    return render_template("ejemplo1.html")

@app.route("/ejemplo2")
def ejemplo2():
    return render_template("ejemplo2.html")

@app.route("/operasBas", methods=["GET", "POST"])
def operasBas():
    if request.method == "POST":
        n1 = request.form.get("n1")
        n2 = request.form.get("n2")
        try:
            n1 = int(n1)
            n2 = int(n2)
            resultado = n1 * n2
            return render_template("resultado.html", n1=n1, n2=n2, resultado=resultado)
        except ValueError:
            return "Error: Ingresa números válidos"
    return render_template("operasBas.html")

@app.route("/hola")
def hola():
    return "<h1> ola de mar </h1>"

@app.route("/user/<string:username>")
def user(username):
    return f"<h1>Hola, {username}!</h1>"

@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El numero es: {n}!</h1>"

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
    return '''
        <form method="POST">  <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre" required>
            <br><br>
            <label for="apellidos">Apellidos:</label>
            <input type="text" id="apellidos" name="apellidos" required>
            <br><br>
            <button type="submit">Enviar</button>
        </form>'''

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
        nombre = request.form.get("nombre")
        cantidad_compradores = request.form.get("cantidad_compradores")
        tarjeta_cineco = request.form.get("tarjeta_cineco")
        cantidad_boletos = request.form.get("cantidad_boletos")

        try:
            cantidad_compradores = int(cantidad_compradores)
            cantidad_boletos = int(cantidad_boletos)

            if cantidad_compradores > MAX_BOLETOS or cantidad_boletos > MAX_BOLETOS or cantidad_boletos != cantidad_compradores:
                raise ValueError("Datos inválidos. Verifica las cantidades y que coincidan.")

            total_compra = cantidad_boletos * PRECIO_BOLETO
            descuento = calcular_descuento(cantidad_boletos, total_compra, tarjeta_cineco == "si")
            total_pagar = total_compra - descuento

            CORTE_TOTAL += total_pagar

            if nombre in REGISTRO_COMPRAS:
                REGISTRO_COMPRAS[nombre][0] += cantidad_boletos
                REGISTRO_COMPRAS[nombre][1] += total_pagar
            else:
                REGISTRO_COMPRAS[nombre] = [cantidad_boletos, total_pagar]

            resultado = {
                "nombre": nombre,
                "cantidad_compradores": cantidad_compradores,
                "cantidad_boletos": cantidad_boletos,
                "tarjeta_cineco": tarjeta_cineco,
                "total": total_pagar
            }

        except ValueError as e:
            resultado = {"error": str(e)}
        except Exception as e:
            resultado = {"error": f"Ocurrió un error: {e}"}

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

signos = [
    "Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey",
    "Tigre", "Conejo", "Dragon", "Serpiente", "Caballo", "Cabra"
]

@app.route('/zod')
def zod():
    return render_template('signo.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dia = int(request.form['dia'])
    mes = int(request.form['mes'])
    anio = int(request.form['anio'])
    sexo = request.form['sexo']

    hoy = datetime.now()
    edad = hoy.year - anio - ((hoy.month, hoy.day) < (mes, dia))

    signo = signos[anio % 12]
    imagen = f"img/{signo.lower()}.jpg"

    return render_template('signo.html', nombre=nombre, apellido=apellido, edad=edad, sexo=sexo, signo=signo, imagen=imagen)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
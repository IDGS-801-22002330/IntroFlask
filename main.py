from flask import Flask, render_template, request, jsonify

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

@app.route("/cinepolis", methods=["GET", "POST"]) #basarse mas en el py de cinepolis, chance y con eso se añaden validaciones y se hace mas dinamico
def cinepolis():
    resultado = None 

    if request.method == "POST":
        nombre = request.form.get("nombre")
        cantidad_compradores = request.form.get("cantidad_compradores")
        tarjeta_cineco = request.form.get("tarjeta_cineco")
        cantidad_boletos = request.form.get("cantidad_boletos")

        try:
            cantidad_compradores = int(cantidad_compradores)
            cantidad_boletos = int(cantidad_boletos)

            precio_boleto = 12
            descuento_cineco = 0.10

            subtotal = cantidad_boletos * precio_boleto

            if tarjeta_cineco == "si":
                descuento = subtotal * descuento_cineco
                total = subtotal - descuento
            else:
                total = subtotal

            resultado = { 
                "total": total
            }

        except Exception as e:
            resultado = {"error": f"Ocurrió un error: {e}"}

    return render_template("cinepolis.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
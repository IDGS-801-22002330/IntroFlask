from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True, port=3000)
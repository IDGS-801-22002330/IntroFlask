from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

signos = [
    "Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey",
    "Tigre", "Conejo", "Dragon", "Serpiente", "Caballo", "Cabra"
]

@app.route('/zod')
def index():
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

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html") 

@app.route("/hola")
def hola():
  return "<h1> ola de mar </h1>"

if __name__ == "__main__":
  app.run(debug=True, port=3000)

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

@app.route("/operas")
def operas():
  return render_template("operas.html")
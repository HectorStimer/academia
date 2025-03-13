from flask import render_template
from main import app

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/registrarUsuario")
def register():
    return render_template("registro-aluno.html")

@app.route("/loginUsuario")
def login():
    return render_template("login.html") 

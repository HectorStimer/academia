from flask import render_template
from main import app
from models import *
from forms import *



@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/registrarUsuario", methods=['GET', 'POST'])
def register():
    form = RegistroAlunoForm()

    if form.validate_on_submit():
        novo_aluno = Aluno(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            data_nascimento=form.data_nascimento.data
        )
        db.session.add(novo_aluno)
        db.session.commit()
        flash("Aluno registrado com sucesso!", "success")
        return redirect(url_for('register'))

    return render_template("registro-aluno.html", form=form)


@app.route("/loginUsuario")
def login():
    return render_template("login.html") 

from flask import render_template, request, redirect, url_for, flash
from main import app, db
from models import Plano, Aluno
from forms import RegistroAlunoForm


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/registrarUsuario", methods=['GET', 'POST'])
def register():
    form = RegistroAlunoForm()
    form.plano_id.choices = [("", "Selecione um Plano")] + [(plano.id_plano, plano.nomePano) for plano in Plano.query.all()]

    if form.validate_on_submit():
        novo_aluno = Aluno(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            data_nascimento=form.data_nascimento.data,
            plano_id=form.plano_id.data,  # Obtendo o ID do plano selecionado
            senha=form.senha.data
        )
        db.session.add(novo_aluno)
        db.session.commit()
        flash('Aluno registrado com sucesso!', 'success')
        return redirect(url_for('homepage'))

    return render_template("registro-aluno.html", form=form)


@app.route("/loginUsuario")
def login():
    return render_template("login.html")

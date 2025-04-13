from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *

registrar_professor_bp = Blueprint('registra_professor', __name__)

@registrar_professor_bp.route("/", methods=['GET', 'POST'])
def registerProfessor():
    form = RegistrarProfessorForm()

    if form.validate_on_submit():

        novo_professor = Professor(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            especialidade=form.especialidade.data
        )
        novo_professor.set_senha(form.senha.data)  

        db.session.add(novo_professor)
        db.session.commit()

        login_user(novo_professor)
        flash('Professor registrado com sucesso!', 'success')

        return redirect(url_for('area_professor.area_professor'))

    return render_template("registrarProfessor.html", form=form)
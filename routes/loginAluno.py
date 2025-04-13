from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *

login_aluno_bp = Blueprint('login_aluno', __name__)


@login_aluno_bp.route("/", methods=['GET', 'POST'])
def loginAluno():
    form = LoginAlunoForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        aluno = Aluno.query.filter_by(email=email).first()

        if not aluno:
            flash('esse usuario nao existe')
            return redirect(url_for('login_aluno.loginAluno'))

        if aluno and aluno.check_senha(senha):
            login_user(aluno, remember=True)
            return redirect(url_for('areaAluno.areaAluno'))

        flash('Email ou senha incorretos', 'danger')
        return redirect(url_for('login_aluno.loginAluno'))
    
    return render_template('login.html', form=form)
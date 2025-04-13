from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *
login_professor_bp = Blueprint('login_professor', __name__)


@login_professor_bp.route('/', methods=['GET', 'POST'])
def loginProfessor():
    form = LoginProfessorForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        if not email:  
            flash('O email não pode ser vazio.', 'danger')
            return redirect(url_for('login_professor.loginProfessor'))
        
        professor = Professor.query.filter_by(email=email).first()

        if not professor:
            flash('esse usuario nao existe')
            return redirect(url_for('login_professor.loginProfessor'))

        if professor and professor.check_senha(senha):
            login_user(professor, remember=True)  # Remova o argumento 'id'
            return redirect(url_for('area_professor.area_professor'))

        flash('Email ou senha incorretos', 'danger')
        return redirect(url_for('login_professor.loginProfessor'))
    
    return render_template('loginProf.html', form=form)
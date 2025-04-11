from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *

registrar_aluno_bp = Blueprint('registrar_aluno', __name__)

def validar_cpf(cpf):
    cpf = ''.join([c for c in cpf if c.isdigit()])
    

    if len(cpf) != 11:
        return False
    

    if cpf == cpf[0] * 11:
        return False
    
    # Calcular o primeiro dígito verificador
    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10) % 11
    if digito1 == 10:
        digito1 = 0

    # Calcular o segundo dígito verificador
    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10) % 11
    if digito2 == 10:
        digito2 = 0
    
    # Verificar se os dígitos verificadores são válidos
    return cpf[-2:] == f"{digito1}{digito2}"


@registrar_aluno_bp.route("/", methods=['GET', 'POST'])
def registrarAluno():
    form = RegistroAlunoForm()

    with app.app_context():
        form.plano_id.choices = [(plano.id_plano, plano.nomePlano) for plano in Plano.query.all()]

    if form.validate_on_submit():
        cpf = form.cpf.data
        
        # Valida o CPF antes de registrar o aluno
        if not validar_cpf(cpf):
            flash('CPF inválido!', 'danger')
            return redirect(url_for('registrarAluno'))

        novo_aluno = Aluno(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            data_nascimento=form.data_nascimento.data,
            plano_id=form.plano_id.data,
            cpf=cpf
        )
        
        novo_aluno.set_senha(form.senha.data)  

        db.session.add(novo_aluno)
        db.session.commit()

        login_user(novo_aluno)
        flash('Aluno registrado com sucesso!', 'success')

        return redirect(url_for('areaAluno'))

    return render_template("registro-aluno.html", form=form)
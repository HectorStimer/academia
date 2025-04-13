from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *

pagamentos_bp = Blueprint('pagamentos', __name__)


@pagamentos_bp.route('/', methods=['GET', 'POST'])
@login_required
def pagamento():
    if not current_user.id_aluno:
        flash("Você precisa ser um aluno para entrar nessa área.", "warning")
        return redirect(url_for('login_aluno.loginAluno'))

    
    plano_atual = Plano.query.filter_by(id_plano=current_user.plano_id).first()

    
    pagamentos = Pagamento.query.filter_by(id_aluno=current_user.id_aluno).all()

    planos = Plano.query.all()

    if request.method == 'POST':
        novo_plano_id = request.form['plano_id']
        
        aluno = Aluno.query.filter_by(id_aluno=current_user.id_aluno).first()
        aluno.plano_id = novo_plano_id
        db.session.commit()

        flash("Plano alterado com sucesso!", "success")
        
       
        plano_atual = Plano.query.filter_by(id_plano=novo_plano_id).first()

    return render_template('pagamentos.html', pagamentos=pagamentos, plano_atual=plano_atual, aluno=current_user, planos=planos)


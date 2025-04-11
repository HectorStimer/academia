from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *

areaAluno_bp = Blueprint('areaAluno', __name__)

@areaAluno_bp.route('/', methods=['GET'])
@login_required
def areaAluno():
    if not current_user.id_aluno: 
        flash("Você precisa ser um aluno para acessar essa área.", "warning")
        return redirect(url_for("loginAluno"))
    
    treinamentos = Treinamento.query.filter_by(id_aluno=current_user.id_aluno).all()
    
    # Dados para o gráfico de progresso
    dados_grafico = {
        'labels': [],
        'datasets': []
    }

    if current_user.progressos:
        dados_grafico['labels'] = [p.data_atualizacao.strftime('%d/%m/%Y') for p in current_user.progressos]
        dados_grafico['datasets'] = [
            {
                'label': 'Peso (kg)',
                'data': [p.peso for p in current_user.progressos],
                'borderColor': 'rgba(54, 162, 235, 1)',
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'fill': False
            },
            {
                'label': 'Cintura (cm)',
                'data': [p.cintura for p in current_user.progressos],
                'borderColor': 'rgba(255, 99, 132, 1)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'fill': False
            }
        ]

    return render_template("areaAluno.html", treinamentos=treinamentos, aluno=current_user, dados_grafico=dados_grafico)
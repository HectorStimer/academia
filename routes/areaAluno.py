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

    ultimo_progresso = None

    if current_user.progressos:
        ultimo_progresso = sorted(current_user.progressos, key=lambda p: p.data_atualizacao, reverse=True)[0]
        dados_grafico['labels'] = [p.data_atualizacao.strftime('%d/%m/%Y') for p in current_user.progressos]
        dados_grafico['datasets'] = [
            {
                'label': 'Peso (kg)',
                'data': [p.peso or 0 for p in current_user.progressos],
                'borderColor': 'rgba(54, 162, 235, 1)',
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'fill': False
            },
            {
                'label': 'Cintura (cm)',
                'data': [p.cintura or 0 for p in current_user.progressos],
                'borderColor': 'rgba(255, 99, 132, 1)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'fill': False
            },
            {
                'label': 'Média Braço (cm)',
                'data': [((p.bracoE or 0) + (p.bracoD or 0)) / 2 for p in current_user.progressos],
                'borderColor': 'rgba(255, 206, 86, 1)',
                'backgroundColor': 'rgba(255, 206, 86, 0.2)',
                'fill': False
            },
            {
                'label': 'Média Coxa (cm)',
                'data': [((p.coxaE or 0) + (p.coxaD or 0)) / 2 for p in current_user.progressos],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'fill': False
            },
            {
                'label': 'Média Panturrilha (cm)',
                'data': [((p.panturrilhaE or 0) + (p.panturrilhaD or 0)) / 2 for p in current_user.progressos],
                'borderColor': 'rgba(153, 102, 255, 1)',
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'fill': False
            },
            {
                'label': 'Tórax (cm)',
                'data': [p.torax or 0 for p in current_user.progressos],
                'borderColor': 'rgba(255, 159, 64, 1)',
                'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                'fill': False
            }
        ]

    return render_template("areaAluno.html", treinamentos=treinamentos, aluno=current_user, dados_grafico=dados_grafico, ultimo_progresso=ultimo_progresso)
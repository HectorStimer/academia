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
            },
            {
                'label': 'Braço Esquerdo (cm)',
                'data': [p.bracoE for p in current_user.progressos],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'fill': False
            },
            {
                'label': 'Braço Direito (cm)',
                'data': [p.bracoD for p in current_user.progressos],
                'borderColor': 'rgba(153, 102, 255, 1)',
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'fill': False
            },
            {
                'label': 'Coxa Esquerda (cm)',
                'data': [p.coxaE for p in current_user.progressos],
                'borderColor': 'rgba(255, 206, 86, 1)',
                'backgroundColor': 'rgba(255, 206, 86, 0.2)',
                'fill': False
            },
            {
                'label': 'Coxa Direita (cm)',
                'data': [p.coxaD for p in current_user.progressos],
                'borderColor': 'rgba(54, 162, 235, 1)',
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'fill': False
            },
            {
                'label': 'Panturrilha Esquerda (cm)',
                'data': [p.panturrilhaE for p in current_user.progressos],
                'borderColor': 'rgba(255, 159, 64, 1)',
                'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                'fill': False
            },
            {
                'label': 'Panturrilha Direita (cm)',
                'data': [p.panturrilhaD for p in current_user.progressos],
                'borderColor': 'rgba(201, 203, 207, 1)',
                'backgroundColor': 'rgba(201, 203, 207, 0.2)',
                'fill': False
            },
            {
                'label': 'Tórax (cm)',
                'data': [p.torax for p in current_user.progressos],
                'borderColor': 'rgba(255, 99, 132, 1)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'fill': False
            }
        ]

    if current_user.id_aluno:
        aluno = Aluno.query.get(current_user.id_aluno)
        if aluno and aluno.progressos:
            dados_grafico['labels'] = [p.data_atualizacao.strftime('%d/%m/%Y') for p in aluno.progressos]
            dados_grafico['datasets'] = [
                {
                    'label': 'Peso (kg)',
                    'data': [p.peso for p in aluno.progressos],
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'fill': False
                },
                # Outros datasets...
            ]
            ultimo_progresso = aluno.progressos[-1]

    return render_template("areaAluno.html", treinamentos=treinamentos, aluno=current_user, dados_grafico=dados_grafico)
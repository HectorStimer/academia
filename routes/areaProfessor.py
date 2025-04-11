from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Aluno, Progresso, Treinamento, Administrador
from forms import TreinamentoForm, ProgressoForm

# Criação do Blueprint
area_professor_bp = Blueprint('area_professor', __name__)

@area_professor_bp.route('/', methods=["GET", "POST"])
@area_professor_bp.route('/''/<int:id_aluno>', methods=["GET", "POST"])
@login_required
def area_professor(id_aluno=None):
    if isinstance(current_user, Aluno): 
        flash("Você precisa ser um professor para acessar esta área.", "warning")
        return redirect(url_for("loginProfessor"))

    admin = Administrador.query.filter_by(id_professor=current_user.id_professor).first()

    form_treinamento = TreinamentoForm()
    form_treinamento.id_aluno.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]

    form_progresso = ProgressoForm()
    form_progresso.id_aluno.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]

    if form_treinamento.validate_on_submit():
        novo_treinamento = Treinamento(
            id_aluno=form_treinamento.id_aluno.data,
            id_professor=current_user.id_professor, 
            treino=form_treinamento.treino.data
        )
        db.session.add(novo_treinamento)
        db.session.commit()
        flash("Treinamento enviado com sucesso!", "success")
        return redirect(url_for("area_professor.area_professor"))

    if form_progresso.validate_on_submit():
        progresso = Progresso(
            id_aluno=form_progresso.id_aluno.data,
            peso=form_progresso.peso.data,
            altura=form_progresso.altura.data,
            bracoE=form_progresso.bracoE.data,
            bracoD=form_progresso.bracoD.data,
            panturrilhaE=form_progresso.panturrilhaE.data,
            panturrilhaD=form_progresso.panturrilhaD.data,
            coxaE=form_progresso.coxaE.data,
            coxaD=form_progresso.coxaD.data,
            torax=form_progresso.torax.data,
            cintura=form_progresso.cintura.data,
            observacoes=form_progresso.observacoes.data
        )
        db.session.add(progresso)
        db.session.commit()
        flash("Progresso registrado com sucesso!", "success")
        return redirect(url_for("area_professor.area_professor", id_aluno=progresso.id_aluno))

    dados_grafico = {
        'labels': [],
        'datasets': []
    }

    if id_aluno:
        aluno = Aluno.query.get(id_aluno)
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
                {
                    'label': 'Cintura (cm)',
                    'data': [p.cintura for p in aluno.progressos],
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'fill': False
                }
            ]

    return render_template('areaProfessor.html', professor=current_user, 
                           form_treinamento=form_treinamento, form_progresso=form_progresso, 
                           admin=admin, dados_grafico=dados_grafico, id_aluno=id_aluno)
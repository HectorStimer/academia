from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Aluno, Progresso, Treinamento, Administrador
from forms import TreinamentoForm, ProgressoForm


area_professor_bp = Blueprint('area_professor', __name__)

@area_professor_bp.route('/', methods=["GET", "POST"])
@login_required
def area_professor():
    # Captura o ID do aluno da URL
    id_aluno = request.args.get('id_aluno', type=int)

    # Verifica se o usuário é um professor
    if isinstance(current_user, Aluno):
        flash("Você precisa ser um professor para acessar esta área.", "warning")
        return redirect(url_for("login_professor.loginProfessor"))

    # Verifica se o professor é um administrador
    admin = Administrador.query.filter_by(id_professor=current_user.id_professor).first()

    # Obter todos os alunos para preencher o campo de seleção
    alunos = Aluno.query.all()
    if not alunos:
        flash("Nenhum aluno encontrado. Adicione alunos antes de enviar treinamentos.", "warning")
        return redirect(url_for("area_professor.area_professor"))

    # Inicializa os formulários
    form_treinamento = TreinamentoForm()
    form_treinamento.id_aluno.choices = [(aluno.id_aluno, aluno.nome) for aluno in alunos]

    form_progresso = ProgressoForm()
    form_progresso.id_aluno.choices = [(aluno.id_aluno, aluno.nome) for aluno in alunos]

    # Buscar treinamentos do aluno selecionado
    treinamentos = []
    aluno = None
    if id_aluno:
        aluno = Aluno.query.get(id_aluno)
        if aluno:
            treinamentos = Treinamento.query.filter_by(id_aluno=id_aluno).all()

    # Se o formulário de treinamento for enviado
    if form_treinamento.validate_on_submit():
        id_aluno = form_treinamento.id_aluno.data
        action = request.form.get("action")

        if action == "enviar":
            # Enviar treinamento
            novo_treinamento = Treinamento(
                id_aluno=id_aluno,
                id_professor=current_user.id_professor,
                treino=form_treinamento.treino.data
            )
            db.session.add(novo_treinamento)
            db.session.commit()
            flash("Treinamento enviado com sucesso!", "success")
        elif action == "deletar":
            # Deletar todos os treinamentos do aluno
            treinamentos = Treinamento.query.filter_by(id_aluno=id_aluno).all()
            if treinamentos:
                for treinamento in treinamentos:
                    db.session.delete(treinamento)  # Marca o treinamento para exclusão
                db.session.commit()  # Confirma a exclusão no banco de dados
                flash("Todos os treinamentos do aluno foram deletados com sucesso!", "success")
            else:
                flash("Nenhum treinamento encontrado para este aluno.", "warning")

            # Atualizar a lista de treinamentos após exclusão
            treinamentos = Treinamento.query.filter_by(id_aluno=id_aluno).all()

        return redirect(url_for("area_professor.area_professor", id_aluno=id_aluno))

    # Se o formulário de progresso for enviado
    if form_progresso.validate_on_submit():
        if id_aluno:
            progresso = Progresso(
                id_aluno=id_aluno,
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
        else:
            flash("Selecione um aluno antes de registrar o progresso.", "warning")
        return redirect(url_for("area_professor.area_professor", id_aluno=id_aluno))

    # Dados para o gráfico e último progresso
    dados_grafico = {'labels': [], 'datasets': []}
    ultimo_progresso = None

    if id_aluno and aluno and aluno.progressos:
        ultimo_progresso = aluno.progressos[-1]
        dados_grafico['labels'] = [p.data_atualizacao.strftime('%d/%m/%Y') for p in aluno.progressos]
        dados_grafico['datasets'] = [
            {
                'label': 'Peso (kg)',
                'data': [p.peso or 0 for p in aluno.progressos],
                'borderColor': 'rgba(54, 162, 235, 1)',
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'fill': False
            },
            {
                'label': 'Cintura (cm)',
                'data': [p.cintura or 0 for p in aluno.progressos],
                'borderColor': 'rgba(255, 99, 132, 1)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'fill': False
            },
            {
                'label': 'Média Braço (cm)',
                'data': [((p.bracoE or 0) + (p.bracoD or 0)) / 2 for p in aluno.progressos],
                'borderColor': 'rgba(255, 206, 86, 1)',
                'backgroundColor': 'rgba(255, 206, 86, 0.2)',
                'fill': False
            },
            {
                'label': 'Média Coxa (cm)',
                'data': [((p.coxaE or 0) + (p.coxaD or 0)) / 2 for p in aluno.progressos],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'fill': False
            },
            {
                'label': 'Média Panturrilha (cm)',
                'data': [((p.panturrilhaE or 0) + (p.panturrilhaD or 0)) / 2 for p in aluno.progressos],
                'borderColor': 'rgba(153, 102, 255, 1)',
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'fill': False
            },
            {
                'label': 'Tórax (cm)',
                'data': [p.torax or 0 for p in aluno.progressos],
                'borderColor': 'rgba(255, 159, 64, 1)',
                'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                'fill': False
            }
        ]

    return render_template('areaProfessor.html',
                           professor=current_user,
                           form_treinamento=form_treinamento,
                           form_progresso=form_progresso,
                           admin=admin,
                           id_aluno=id_aluno,
                           aluno=aluno,
                           treinamentos=treinamentos,
                           ultimo_progresso=ultimo_progresso,
                           dados_grafico=dados_grafico)
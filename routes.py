from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, current_user, logout_user
from main import app, lm, db
from models import *
from forms import *

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


@lm.user_loader
def user_loader(user_id):
    aluno = Aluno.query.get(user_id)
    if aluno:
        return aluno

    professor = Professor.query.get(user_id)
    if professor:
        return professor

    return None

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/register/aluno", methods=['GET', 'POST'])


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


@app.route("/register/professor", methods=['GET', 'POST'])
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

        return redirect(url_for('areaProfessor'))

    return render_template("registrarProfessor.html", form=form)


@app.route("/login/aluno", methods=['GET', 'POST'])
def loginAluno():
    form = LoginAlunoForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        aluno = Aluno.query.filter_by(email=email).first()

        if not aluno:
            flash('esse usuario nao existe')
            return redirect(url_for('loginAluno'))

        if aluno and aluno.check_senha(senha):
            login_user(aluno)
            return redirect(url_for('areaAluno'))

        flash('Email ou senha incorretos', 'danger')
        return redirect(url_for('loginAluno'))
    
    return render_template('login.html', form=form)





@app.route('/login/professor', methods=['GET', 'POST'])
def loginProfessor():
    form = LoginProfessorForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        if not email:  
            flash('O email não pode ser vazio.', 'danger')
            return redirect(url_for('loginProfessor'))
        
        professor = Professor.query.filter_by(email=email).first()

        if not professor:
            flash('esse usuario nao existe')
            return redirect(url_for('loginProfessor'))

        if professor and professor.check_senha(senha):
            login_user(professor)
            return redirect(url_for('areaProfessor'))

        flash('Email ou senha incorretos', 'danger')
        return redirect(url_for('loginProfessor'))
    
    return render_template('loginProf.html', form=form)


@app.route('/area/aluno', methods=['GET'])
@login_required
def areaAluno():
    if not current_user.id_aluno: 
        flash("Você precisa ser um aluno para acessar essa área.", "warning")
        return redirect(url_for("loginAluno"))
    

    treinamentos = Treinamento.query.filter_by(id_aluno=current_user.id_aluno).all()

    return render_template("areaAluno.html", treinamentos=treinamentos, aluno=current_user)

@app.route('/pagamentos', methods=['GET', 'POST'])
@login_required
def pagamento():
    if not current_user.id_aluno:
        flash("Você precisa ser um aluno para entrar nessa área.", "warning")
        return redirect(url_for('loginAluno'))

    
    plano_atual = Plano.query.filter_by(id_plano=current_user.plano_id).first()

    
    pagamentos = Pagamento.query.filter_by(id_aluno=current_user.id_aluno).all()

    planos = Plano.query.all()

    if request.method == 'POST':
        novo_plano_id = request.form['plano_id']
        
        aluno = Aluno.query.filter_by(id_aluno=current_user.id_aluno).first()
        aluno.plano_id = novo_plano_id
        db.session.commit()

        flash("Plano alterado com sucesso!", "success")
        
        # Atualiza o plano atual com o novo plano
        plano_atual = Plano.query.filter_by(id_plano=novo_plano_id).first()

    return render_template('pagamentos.html', pagamentos=pagamentos, plano_atual=plano_atual, aluno=current_user, planos=planos)



@app.route("/logout")
@login_required
def logout():
    user_type = type(current_user) 

    logout_user()
    flash("Você saiu da sua conta.", "info")

    if user_type == Professor:
        return redirect(url_for("loginProfessor"))
    return redirect(url_for("loginAluno"))


@app.route('/area/professor', methods=["GET", "POST"])
@app.route('/area/professor/<int:id_aluno>', methods=["GET", "POST"])
@login_required
def areaProfessor(id_aluno=None):
    # Verifica se o usuário logado é um professor
    if isinstance(current_user, Aluno): 
        flash("Você precisa ser um professor para acessar esta área.", "warning")
        return redirect(url_for("loginProfessor"))

    # Verifica se o professor é administrador
    admin = Administrador.query.filter_by(id_professor=current_user.id_professor).first()

    # Formulário de Treinamento
    form_treinamento = TreinamentoForm()
    form_treinamento.id_aluno.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]

    # Formulário de Progresso
    form_progresso = ProgressoForm()
    form_progresso.id_aluno.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]

    # Processa o formulário de treinamento
    if form_treinamento.validate_on_submit():
        novo_treinamento = Treinamento(
            id_aluno=form_treinamento.id_aluno.data,
            id_professor=current_user.id_professor, 
            treino=form_treinamento.treino.data
        )
        db.session.add(novo_treinamento)
        db.session.commit()
        flash("Treinamento enviado com sucesso!", "success")
        return redirect(url_for("areaProfessor"))

    # Processa o formulário de progresso
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
        return redirect(url_for("areaProfessor", id_aluno=progresso.id_aluno))

    # Dados do gráfico
    dados_grafico = {
        'labels': ['Antes', 'Depois'],
        'datasets': []
    }

    if id_aluno:  # Filtra os dados apenas do aluno selecionado
        aluno = Aluno.query.get(id_aluno)
        if aluno and aluno.progressos and len(aluno.progressos) >= 2:
            progresso_antes = aluno.progressos[0]
            progresso_depois = aluno.progressos[-1]

            medidas_antes = [
                progresso_antes.bracoE, progresso_antes.bracoD, progresso_antes.panturrilhaE,
                progresso_antes.panturrilhaD, progresso_antes.coxaE, progresso_antes.coxaD,
                progresso_antes.torax, progresso_antes.cintura
            ]
            medidas_depois = [
                progresso_depois.bracoE, progresso_depois.bracoD, progresso_depois.panturrilhaE,
                progresso_depois.panturrilhaD, progresso_depois.coxaE, progresso_depois.coxaD,
                progresso_depois.torax, progresso_depois.cintura
            ]

            medidas_antes = [m for m in medidas_antes if m is not None]
            medidas_depois = [m for m in medidas_depois if m is not None]

            media_antes = sum(medidas_antes) / len(medidas_antes) if medidas_antes else 0
            media_depois = sum(medidas_depois) / len(medidas_depois) if medidas_depois else 0

            dados_grafico['datasets'].append({
                'label': f'{aluno.nome} - Peso (kg)',
                'data': [progresso_antes.peso, progresso_depois.peso],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            })
            dados_grafico['datasets'].append({
                'label': f'{aluno.nome} - Média das Medidas (cm)',
                'data': [media_antes, media_depois],
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1
            })

    return render_template('areaProfessor.html', professor=current_user, 
                           form_treinamento=form_treinamento, form_progresso=form_progresso, 
                           admin=admin, dados_grafico=dados_grafico, id_aluno=id_aluno)



@app.route("/administracao", methods=["GET", "POST"])
@login_required
def Admin():
    admin = Administrador.query.filter_by(id_professor=current_user.id_professor).first()

    if not admin:
        flash("Você não tem permissão para acessar esta área.", "warning")
        return redirect(url_for("areaProfessor"))

    form = AdminForm()
    form.aluno_id.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]

    if form.validate_on_submit():
        aluno_id = form.aluno_id.data
        aluno = Aluno.query.get(aluno_id)

        if aluno:
            # Atualiza os dados do aluno
            aluno.nome = form.nome.data
            aluno.email = form.email.data
            aluno.status = form.status.data
            aluno.pagamento = form.pagamento.data

            # Atualiza a senha com hash
            if form.senha.data:
                aluno.set_senha(form.senha.data)

            try:
                db.session.commit()
                flash(f"Dados do aluno {aluno.nome} atualizados com sucesso!", "success")
            except Exception as e:
                db.session.rollback()
                flash("Erro ao atualizar os dados do aluno. Tente novamente.", "danger")
        else:
            flash("Aluno não encontrado.", "danger")

        return redirect(url_for('Admin'))

    return render_template('administracao.html', form=form, admin=admin)
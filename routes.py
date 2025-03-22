from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from main import app, lm, db
from models import *
from forms import *

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

# Registro do Aluno
@app.route("/registrarAluno", methods=['GET', 'POST'])
def registrarAluno():
    form = RegistroAlunoForm()

    with app.app_context():
        form.plano_id.choices = [(plano.id_plano, plano.nomePlano) for plano in Plano.query.all()]

    if form.validate_on_submit():
        # Criptografar a senha
        senha_hash = generate_password_hash(form.senha.data)

        novo_aluno = Aluno(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            data_nascimento=form.data_nascimento.data,
            plano_id=form.plano_id.data,  
            senha=senha_hash  
        )

        db.session.add(novo_aluno)
        db.session.commit()

        login_user(novo_aluno)  # Agora pode logar o aluno
        flash('Aluno registrado com sucesso!', 'success')

        return redirect(url_for('homepage'))

    return render_template("registro-aluno.html", form=form)

# Registro do Professor
@app.route("/registrarProfessor", methods=['GET', 'POST'])
def registerProfessor():
    form = RegistrarProfessorForm()

    if form.validate_on_submit():
        # Criptografar a senha
        senha_hash = generate_password_hash(form.senha.data)

        novo_professor = Professor(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            especialidade=form.especialidade.data,
            senha=senha_hash  # Armazenando a senha criptografada
        )

        db.session.add(novo_professor)
        db.session.commit()

        login_user(novo_professor)
        flash('Professor registrado com sucesso!', 'success')

        return redirect(url_for('areaProfessor'))

    return render_template("registro-professor.html", form=form)

@app.route("/loginAluno", methods=['GET', 'POST'])
def loginAluno():
    form = LoginAlunoForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        aluno = Aluno.query.filter_by(email=email).first()

        if aluno and aluno.check_senha(senha):  
            login_user(aluno)
            return redirect(url_for('areaAluno'))

        flash('Email ou senha incorretos', 'danger')
        return redirect(url_for('loginAluno'))
    
    return render_template('login.html', form=form)




@app.route('/loginProfessor', methods=['GET', 'POST'])
def loginProfessor():
    form = LoginProfessorForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        professor = Professor.query.filter_by(email=email).first()

        if professor and professor.check_senha(senha): 
            login_user(professor)
            return redirect(url_for('areaProfessor'))

        flash('Email ou senha incorretos', 'danger')
        return redirect(url_for('loginProfessor'))
    
    return render_template('loginProf.html', form=form)


@app.route('/areaAluno', methods=['GET'])
@login_required
def areaAluno():
    if not current_user.is_aluno(): 
        flash("Você precisa ser um aluno para acessar essa área.", "warning")
        return redirect(url_for("loginAluno"))

    treinamentos = Treinamento.query.filter_by(aluno_id=current_user.id_aluno).all()

    return render_template("areaAluno.html", treinamentos=treinamentos, aluno=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")

    if isinstance(current_user, Professor):
        return redirect(url_for("loginProfessor"))
    return redirect(url_for("loginAluno"))

@app.route('/areaProfessor', methods=["GET", "POST"])
@login_required
def areaProfessor():
    if not current_user.is_professor(): 
        flash("Você precisa ser um professor para acessar esta área.", "warning")
        return redirect(url_for("loginProfessor"))

    form = TreinamentoForm()
    form.id_aluno.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]

    return render_template('areaProfessor.html', professor=current_user, form=form)

@app.route('/enviarTreinamento', methods=['POST'])
def enviarTreinamento():
    form = TreinamentoForm()
    form.id_aluno.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]

    if form.validate_on_submit():
        novo_Treinamento = Treinamento(
            aluno_id=form.id_aluno.data,
            treino=form.treino.data
        )
        db.session.add(novo_Treinamento)
        db.session.commit()

        flash("Treinamento enviado com sucesso!", "success")
        return redirect(url_for('areaProfessor'))

    flash("Erro ao enviar treinamento", "danger")
    return redirect(url_for('areaProfessor'))

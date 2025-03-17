from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, LoginManager, UserMixin,login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from main import app, lm, db
from models import *
from forms import *


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/registrarUsuario", methods=['GET', 'POST'])
def register():
    form = RegistroAlunoForm()
    
    with app.app_context():
        form.plano_id.choices = [(plano.id_plano, plano.nomePlano) for plano in Plano.query.all()]
    
    if form.validate_on_submit():
        novo_aluno = Aluno(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            data_nascimento=form.data_nascimento.data,
            plano_id=form.plano_id.data,  
            senha=form.senha.data # Criptografa a senha
        )

        db.session.add(novo_aluno)
        db.session.commit()

        login_user(novo_aluno)  # Agora pode logar o aluno
        flash('Aluno registrado com sucesso!', 'success')
        
        return redirect(url_for('homepage'))

    return render_template("registro-aluno.html", form=form)



@app.route("/loginAluno", methods=['GET', 'POST'])
def loginAluno():
    form = LoginAlunoForm()
    
    if form.validate_on_submit():
        aluno = Aluno.query.filter_by(email=form.email.data).first()  
        if aluno and (aluno.senha == form.senha.data):
            session['id_aluno'] = aluno.id_aluno
            flash("Login realizado com sucesso", "success")
            return redirect(url_for('areaAluno'))
        flash('Email ou senha incorretos', 'danger')
    
    return render_template("login.html", form=form)


@lm.user_loader
def user_loader(user_id):
    aluno = Aluno.query.get(user_id)
    if aluno:
        return aluno

    professor = Professor.query.get(user_id)
    if professor:
        return professor

    return None 




@app.route('/loginProfessor', methods=['GET', 'POST'])
def loginProfessor():
    form = LoginProfessorForm() 

    if form.validate_on_submit(): 
        email = form.email.data  
        senha = form.senha.data

        professor = Professor.query.filter_by(email=email).first()

        if professor and (professor.senha == senha):  
            login_user(professor)
            return redirect(url_for('areaProfessor'))  

        flash('Email ou senha incorretos', 'danger')
        return redirect(url_for('loginProfessor'))  
    return render_template('loginProf.html', form=form) 


        
@app.route('/areaProfessor', methods=["GET", "POST"])
@login_required
def areaProfessor():
    if not isinstance(current_user, Professor):
        flash("Você precisa ser um professor para acessar esta área.", "warning")
        return redirect(url_for("loginProfessor"))

    alunos = Aluno.query.all()  # Todos os alunos
    progresso = {aluno.id_aluno: Progresso.query.filter_by(id_aluno=aluno.id_aluno).all() for aluno in alunos}
    
    form = TreinamentoForm()  

    return render_template('areaProfessor.html', professor=current_user, alunos=alunos, progresso_alunos=progresso, form=form)


@app.route('/enviarTreinamento', methods=['POST'])
def enviarTreinamento():
    form = TreinamentoForm()
    
    if form.validate_on_submit():
        novo_treinamento = Treinamento(
            treino=form.treino.data,
            id_aluno=form.id_aluno.data,
            id_professor=current_user.id_professor  
        )
        
        db.session.add(novo_treinamento)
        db.session.commit()
        
        flash("Treinamento enviado com sucesso!", "success")
        return redirect(url_for('areaProfessor'))
    
    flash("Erro ao enviar treinamento", "danger")
    return redirect(url_for('areaProfessor', form=form))
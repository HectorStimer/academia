from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from main import app, db
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
            senha=form.senha.data
        )
        db.session.add(novo_aluno)
        db.session.commit()
        flash('Aluno registrado com sucesso!', 'success')
        return redirect(url_for('homepage'))

    return render_template("registro-aluno.html", form=form)


@app.route("/loginAluno", methods=['GET', 'POST'])
def loginAluno():
    form = LoginAlunoForm()
    
    if form.validate_on_submit():
        aluno = Aluno.query.filter_by(email=form.email.data).first()  
        if aluno and check_password_hash(aluno.senha, form.senha.data):
            session['id_aluno'] = aluno.id_aluno
            flash("Login realizado com sucesso", "success")
            return redirect(url_for('areaAluno'))
        flash('Email ou senha incorretos', 'danger')
    
    return render_template("login.html", form=form)


@app.route("/loginProfessor", methods=['GET', 'POST'])
def loginProfessor():
    form = LoginProfessorForm()  # Certifique-se de instanciar o formulário
    if request.method == "GET":
        return render_template('loginProf.html', form=form)  # Passando o form para o template

    elif request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']

        # Busca o professor no banco de dados
        professor = db.session.query(Professor).filter_by(email=email).first()

        # Verifica se o professor existe e a senha está correta
        if professor and check_password_hash(professor.senha, senha):
            session["id_professor"] = professor.id_professor  # Armazena o id do professor na sessão
            flash("Login realizado com sucesso", "success")
            return redirect(url_for('areaProfessor'))  # Redireciona para a área do professor
        else:
            flash("Email ou senha incorretos", "danger")  # Exibe a mensagem de erro
            return redirect(url_for('loginProfessor'))  # Redireciona de volta para o login

        
@app.route('/areaProfessor')
def areaProfessor():
    if "id_professor" not in session: 
        flash("Você precisa fazer login para acessar essa área.", "warning")
        return redirect(url_for("loginProfessor"))  

    id_professor = session['id_professor']
    professor = Professor.query.get(id_professor)

    alunos = Aluno.query.all()  # Todos os alunos

    progresso = {aluno.id_aluno: Progresso.query.filter_by(id_aluno=aluno.id_aluno).all() for aluno in alunos}

    return render_template('areaProfessor.html', professor=professor, alunos=alunos, progresso_alunos=progresso)



@app.route('/enviarTreinamento', methods=['POST'])
def enviarTreinamento():
    form = TreinamentoForm()
    
    if form.validate_on_submit():
        novo_treinamento = Treinamento(
            treino=form.treino.data,
            id_aluno=form.id_aluno.data,
            id_professor=session.get('id_professor')
        )
        
        db.session.add(novo_treinamento)
        db.session.commit()
        
        flash("Treinamento enviado com sucesso!", "success")
        return redirect(url_for('areaProfessor'))
    
    flash("Erro ao enviar treinamento", "danger")
    return redirect(url_for('areaProfessor'))

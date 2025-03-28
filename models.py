from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Aluno(db.Model, UserMixin):
    __tablename__ = 'alunos'
    
    id_aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.Integer, nullable = False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(14))
    data_nascimento = db.Column(db.Date)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id_plano'), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False) 
    status = db.Column(db.Boolean, default=False)

    def set_senha(self, senha):
        
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def get_id(self):
        return str(self.id_aluno)

class Pagamento(db.Model, UserMixin):
    __tablename__ = 'pagamento'  

    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)

    aluno = db.relationship('Aluno', backref=db.backref('pagamentos', lazy=True, cascade="all, delete-orphan"))

class Professor(db.Model, UserMixin):
    __tablename__ = 'professores' 

    id_professor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)  
    telefone = db.Column(db.String(14))
    especialidade = db.Column(db.String(20))
    senha_hash = db.Column(db.String(255), nullable=False) 

    def set_senha(self, senha):
        
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def get_id(self):
        return str(self.id_professor)

class Treinamento(db.Model, UserMixin):
    __tablename__ = 'treinamentos'

    id_treinamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professores.id_professor'), nullable=False)  # Alterado para "professores"
    treino = db.Column(db.Text, nullable=False)

    aluno = db.relationship('Aluno', backref=db.backref('treinamentos', lazy=True, cascade="all, delete-orphan"))
    professor = db.relationship('Professor', backref=db.backref('treinamentos', lazy=True, cascade="all, delete-orphan"))

class Plano(db.Model, UserMixin):
    __tablename__ = 'planos'

    id_plano = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomePlano = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

class Progresso(db.Model, UserMixin):
    __tablename__ = 'progressos'
    
    id_progresso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    peso = db.Column(db.Numeric(5, 2), nullable=True)  # Exemplo: 70.5 kg
    altura = db.Column(db.Numeric(4, 2), nullable=True)  # Exemplo: 1.75 m
    bracoE = db.Column(db.Numeric(4,2), nullable= True)
    bracoD = db.Column(db.Numeric(4,2), nullable= True)
    panturrilhaE = db.Column(db.Numeric(4,2), nullable= True)
    panturrilhaD = db.Column(db.Numeric(4,2), nullable= True)
    coxaE = db.Column(db.Numeric(4,2), nullable= True)
    coxaD = db.Column(db.Numeric(4,2), nullable= True)
    torax = db.Column(db.Numeric(4,2), nullable= True)
    cintura = db.Column(db.Numeric(4,2), nullable= True)
    observacoes = db.Column(db.Text, nullable=True)  # Comentários sobre o progresso

    aluno = db.relationship('Aluno', backref=db.backref('progressos', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<Progresso {self.id_progresso} - Aluno {self.id_aluno}>'


class Administrador(db.Model, UserMixin):
    __tablename__ = "administrador"

    id_ADM= db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_professor = db.Column(db.Integer, db.ForeignKey('professores.id_professor'), nullable=False)

    

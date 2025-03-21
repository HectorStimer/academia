from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Aluno(db.Model, UserMixin):
    __tablename__ = 'alunos'
    
    id_aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(14))
    data_nascimento = db.Column(db.Date)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id_plano'), nullable=False)
    senha = db.Column(db.String(225), nullable=False)  # Alterado para 100 para permitir senhas maiores

    def get_id(self):
        return str(self.id_aluno)

    # Aqui criamos o método para verificar a senha fornecida no login
    def check_senha(self, senha_fornecida):
        return check_password_hash(self.senha, senha_fornecida)

class Pagamento(db.Model, UserMixin):
    __tablename__ = 'pagamento'  

    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)

    aluno = db.relationship('Aluno', backref=db.backref('pagamentos', lazy=True, cascade="all, delete-orphan"))

class Professor(db.Model, UserMixin):
    __tablename__ = 'professores'  # Alterado para "professores" (plural para manter a consistência)

    id_professor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)  # Corrigido para manter a definição de "email"
    telefone = db.Column(db.String(14))
    especialidade = db.Column(db.String(20))
    senha = db.Column(db.String(225), nullable=False)  # Alterado para 100 para permitir senhas maiores

    def get_id(self):
        return str(self.id_professor)

    # Aqui criamos o método para verificar a senha fornecida no login
    def check_senha(self, senha_fornecida):
        return check_password_hash(self.senha, senha_fornecida) 

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
    __tablename__ = 'progresso'
    
    id_progresso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    progresso = db.Column(db.String(200), nullable=True)

    aluno = db.relationship('Aluno', backref=db.backref('progresso', lazy=True))

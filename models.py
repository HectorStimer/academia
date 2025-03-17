from main import db
from flask_login import UserMixin

class Aluno(db.Model,UserMixin):
    __tablename__ = 'alunos'
    
    id_aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(14))
    data_nascimento = db.Column(db.Date)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id_plano'), nullable=False)
    senha = db.Column(db.String(30), nullable=False)

    def get_id(self):
        return str(self.id_aluno)  

class Pagamento(db.Model, UserMixin):
    __tablename__ = 'pagamento'  

    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column(db.Numeric(10,2), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)

    aluno = db.relationship('Aluno', backref=db.backref('pagamentos', lazy=True, cascade="all, delete-orphan"))

class Professor(db.Model,UserMixin):
    __tablename__ = 'professor'

    id_professor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(14))
    especialidade = db.Column(db.String(20))
    email= db.Column(db.String(100), nullable=False, unique= True)
    senha= db.Column(db.String(30), nullable=False)

    def get_id(self):
        return str(self.id_professor)  

class Treinamento(db.Model,UserMixin):
    __tablename__ = 'treinamento'

    id_treinamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id_professor'), nullable=False)
    treino = db.Column(db.Text, nullable=False)

    aluno = db.relationship('Aluno', backref=db.backref('treinamentos', lazy=True, cascade="all, delete-orphan"))
    professor = db.relationship('Professor', backref=db.backref('treinamentos', lazy=True, cascade="all, delete-orphan"))

class Plano(db.Model,UserMixin):
    __tablename__ = 'planos'

    id_plano = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomePlano = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)


class Progresso(db.Model,UserMixin):
    __tablename__ = 'progresso'
    
    id_progresso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    progresso = db.Column(db.String(200), nullable=True)

    aluno = db.relationship('Aluno', backref=db.backref('progresso', lazy=True))

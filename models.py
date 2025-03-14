from main import db

class Aluno(db.Model):
    __tablename__ = 'alunos'
    
    id_aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(14))
    data_nascimento = db.Column(db.Date)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id_plano'), nullable=False)
    senha = db.Column(db.String(30), nullable=False)

class Pagamento(db.Model):
    __tablename__ = 'pagamento'  

    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column(db.Numeric(10,2), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)

    aluno = db.relationship('Aluno', backref=db.backref('pagamentos', lazy=True, cascade="all, delete-orphan"))

class Professor(db.Model):
    __tablename__ = 'professor'

    id_professor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(14))
    especialidade = db.Column(db.String(20))

class Treinamento(db.Model):
    __tablename__ = 'treinamento'

    id_treinamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id_professor'), nullable=False)
    treino = db.Column(db.Text, nullable=False)

    aluno = db.relationship('Aluno', backref=db.backref('treinamentos', lazy=True, cascade="all, delete-orphan"))
    professor = db.relationship('Professor', backref=db.backref('treinamentos', lazy=True, cascade="all, delete-orphan"))

class Plano(db.Model):
    __tablename__ = 'planos'

    id_plano = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomePlano = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

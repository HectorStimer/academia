from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_login import login_manager

class RegistroAlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Length(max= 100), Email(message='Email inválido'),Length(min=6,max= 30)])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('confirmar', message="As senhas devem ser iguais."),Length(min=6,max= 30)])
    confirmar = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message="As senhas devem ser iguais."),Length(min=6,max= 30)])
    telefone = StringField('Telefone', validators=[DataRequired(message='Precisamos de seu telefone para contato'),Length(max=11)])
    cpf=StringField('CPF', validators=[DataRequired(message= 'Precisamos do seu CPF'), Length(min= 11, max = 14)])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d')
    plano_id = SelectField('Plano', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar')

class RegistrarProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Length(max= 100), Email(message='Email inválido'),Length(min=6,max= 50)])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('confirmar', message="As senhas devem ser iguais."),Length(min=6,max= 30)])
    confirmar = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message="As senhas devem ser iguais."),Length(min=6,max= 30)])
    telefone = StringField('Telefone', validators=[DataRequired(message='Precisamos de seu telefone para contato'),Length(max=11)])
    especialidade = StringField('Especialidade', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Registrar')
    

class LoginProfessorForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message = 'Email do professor invalido no DB')])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class LoginAlunoForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message = 'Email do professor invalido no DB')])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField("Entrar")

class TreinamentoForm(FlaskForm):
    id_aluno = SelectField('ID do Aluno', validators=[DataRequired()], coerce=int) 
    treino = TextAreaField('Treinamento', validators=[DataRequired()])
    submit = SubmitField('Enviar Treinamento')


class receberTreinamentoForm(FlaskForm):
    id_professor = StringField()
    Treinamento = TextAreaField()


class ProgressoForm(FlaskForm):
    id_aluno = SelectField('ID do Aluno', validators=[Optional()])
    peso = DecimalField('Peso (kg)', validators=[Optional()], places=2)
    altura = DecimalField('Altura (m)', validators=[Optional()], places=2)
    bracoE = DecimalField('Braço Esquerdo (cm)', validators=[Optional()], places=2)
    bracoD = DecimalField('Braço Direito (cm)', validators=[Optional()], places=2)
    panturrilhaE = DecimalField('Panturrilha Esquerda (cm)', validators=[Optional()], places=2)
    panturrilhaD = DecimalField('Panturrilha Direita (cm)', validators=[Optional()], places=2)
    torax = DecimalField('Tórax (cm)', validators=[Optional()], places=2)
    cintura = DecimalField('Cintura (cm)', validators=[Optional()], places=2)
    coxaE = DecimalField('Coxa Esquerda (cm)', validators=[Optional()], places=2)
    coxaD = DecimalField('Coxa Direita (cm)', validators=[Optional()], places=2)
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Registrar Progresso')

class AdminForm(FlaskForm):
    aluno_id = SelectField("Aluno", coerce=int, validators=[DataRequired()])  # Campo para selecionar o aluno
    nome = StringField("Nome", validators=[Optional(), Length(min=2, max=100)])
    email = StringField("Email", validators=[Optional(), Email()])
    telefone = StringField("Telefone", validators=[Optional(), Length(max=11)])
    cpf = StringField("CPF", validators=[Optional(), Length(min=11, max=14)])
    data_nascimento = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[Optional()])
    plano_id = SelectField("Plano", coerce=int, validators=[Optional()])
    status = SelectField("Status", choices=[("ativo", "Ativo"), ("inativo", "Inativo")], validators=[Optional()])
    mes_pagamento = SelectField("Mês de Pagamento", choices=[
        ("Janeiro", "Janeiro"), ("Fevereiro", "Fevereiro"), ("Março", "Março"), ("Abril", "Abril"),
        ("Maio", "Maio"), ("Junho", "Junho"), ("Julho", "Julho"), ("Agosto", "Agosto"),
        ("Setembro", "Setembro"), ("Outubro", "Outubro"), ("Novembro", "Novembro"), ("Dezembro", "Dezembro")
    ], validators=[Optional()])
    status_pagamento = SelectField("Status do Pagamento", choices=[("pago", "Pago"), ("nao_pago", "Não Pago")], validators=[Optional()])
    senha = PasswordField("Senha", validators=[Optional(), Length(min=6, max=30)])  # Senha opcional
    submit = SubmitField("Atualizar")
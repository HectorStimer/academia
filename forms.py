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
    id_aluno = SelectField('ID do Aluno', validators=[DataRequired()])
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
    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=100)])
    senha = StringField("Senha", validators=[DataRequired(), Length(min=6, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    status = SelectField("Status", choices=[("ativo", "Ativo"), ("inativo", "Inativo")])
    pagamento = SelectField("Pagamento", choices=[("pago", "Pago"), ("pendente", "Pendente")])
    submit = SubmitField("Atualizar")
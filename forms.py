from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class RegistroAlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Length(max= 100), Email(message='Email inválido'),Length(min=6,max= 30)])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('confirmar', message="As senhas devem ser iguais."),Length(min=6,max= 30)])
    confirmar = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message="As senhas devem ser iguais."),Length(min=6,max= 30)])
    telefone = StringField('Telefone', validators=[DataRequired(message='Precisamos de seu telefone para contato'),Length(max=11)])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d')
    plano_id = SelectField('Plano', coerce=int, validators=[DataRequired()])
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
    id_aluno = IntegerField('ID do Aluno', validators=[DataRequired()])
    treino = TextAreaField('Treinamento', validators=[DataRequired()])
    submit = SubmitField('Enviar Treinamento')








    

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistroAlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Email inválido')])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('confirmar', message="As senhas devem ser iguais.")])
    confirmar = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message="As senhas devem ser iguais.")])
    telefone = StringField('Telefone', validators=[DataRequired(message='Precisamos de seu telefone para contato')])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d')
    plano_id = SelectField('Plano', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar')

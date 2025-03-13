from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class RegistroAlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=30)])
    telefone = StringField('Telefone')
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d')
    submit = SubmitField('Registrar')

from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *

from .administracao import admin_bp
from .areaAluno import areaAluno_bp
from .areaProfessor import area_professor_bp
from .homepage import homepage_bp
from .loginAluno import login_aluno_bp
from .loginProfessor import login_professor_bp
from .logout import logout_bp
from .pagamentos import pagamentos_bp
from .registrarProfessor import registrar_professor_bp
from .registrarAluno import registrar_aluno_bp
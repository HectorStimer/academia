from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *

logout_bp = Blueprint('logout', __name__)

@logout_bp.route("/logout")
@login_required
def logout():
    user_type = type(current_user) 

    logout_user()
    flash("Você saiu da sua conta.", "info")

    if user_type == Professor:
        return redirect(url_for("login_professor.loginProfessor"))
    return redirect(url_for("login_aluno.loginAluno"))

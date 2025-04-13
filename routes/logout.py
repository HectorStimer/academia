from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from flask import current_app as app
from extensions import db, lm
from models import *
from forms import *

logout_bp = Blueprint('logout', __name__)

@logout_bp.route("/")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("homepage.homepage"))

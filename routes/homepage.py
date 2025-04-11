from flask import Flask, render_template, redirect, url_for, request, Blueprint
from flask import current_app as app

homepage_bp = Blueprint('homepage', __name__)

@homepage_bp.route("/")
def homepage():
    return render_template("index.html")


from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Administrador, Aluno
from forms import AdminForm

# Criação do Blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/", methods=["GET", "POST"])
@login_required
def admin_dashboard():
    admin = Administrador.query.filter_by(id_professor=current_user.id_professor).first()

    if not admin:
        flash("Você não tem permissão para acessar esta área.", "warning")
        return redirect(url_for("areaProfessor"))

    form = AdminForm()
    form.aluno_id.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]

    if form.validate_on_submit():
        aluno_id = form.aluno_id.data
        aluno = Aluno.query.get(aluno_id)

        if aluno:
            aluno.nome = form.nome.data
            aluno.email = form.email.data
            aluno.status = form.status.data
            aluno.pagamento = form.pagamento.data

            if form.senha.data:
                aluno.set_senha(form.senha.data)

            try:
                db.session.commit()
                flash(f"Dados do aluno {aluno.nome} atualizados com sucesso!", "success")
            except Exception:
                db.session.rollback()
                flash("Erro ao atualizar os dados do aluno. Tente novamente.", "danger")
        else:
            flash("Aluno não encontrado.", "danger")

        return redirect(url_for('admin.admin_dashboard'))

    return render_template('administracao.html', form=form, admin=admin)
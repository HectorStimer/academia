from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Administrador, Aluno, Pagamento, Plano
from forms import AdminForm

# Criação do Blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/", methods=["GET", "POST"])
@login_required
def admin_dashboard():
    admin = Administrador.query.filter_by(id_professor=current_user.id_professor).first()

    if not admin:
        flash("Você não tem permissão para acessar esta área.", "warning")
        return redirect(url_for("area_professor.area_professor"))

    form = AdminForm()
    form.aluno_id.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]
    form.plano_id.choices = [(plano.id_plano, plano.nomePlano) for plano in Plano.query.all()]

    if form.validate_on_submit():
        aluno_id = form.aluno_id.data
        aluno = Aluno.query.get(aluno_id)

        if aluno:
            # Atualizar os dados do aluno
            aluno.nome = form.nome.data
            aluno.email = form.email.data
            aluno.telefone = form.telefone.data
            aluno.cpf = form.cpf.data
            aluno.data_nascimento = form.data_nascimento.data
            aluno.plano_id = form.plano_id.data
            aluno.status = form.status.data == "ativo"  # Converte para booleano

            # Atualizar o status de pagamento do mês
            mes_pagamento = form.mes_pagamento.data
            status_pagamento = form.status_pagamento.data

            if mes_pagamento and status_pagamento:
                pagamento = Pagamento.query.filter_by(id_aluno=aluno.id_aluno, mes=mes_pagamento).first()
                if not pagamento:
                    pagamento = Pagamento(id_aluno=aluno.id_aluno, mes=mes_pagamento, status=status_pagamento)
                    db.session.add(pagamento)
                else:
                    pagamento.status = status_pagamento

            # Atualizar a senha, se fornecida
            if form.senha.data:
                aluno.set_senha(form.senha.data)

            try:
                db.session.commit()
                flash(f"Dados do aluno {aluno.nome} atualizados com sucesso!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao atualizar os dados do aluno: {str(e)}", "danger")
        else:
            flash("Aluno não encontrado.", "danger")

        return redirect(url_for('admin.admin_dashboard'))

    return render_template('administracao.html', form=form, admin=admin)
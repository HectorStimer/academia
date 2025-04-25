from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Administrador, Aluno, Pagamento, Plano
from forms import AdminForm, PagamentoForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/", methods=["GET", "POST"])
@login_required
def admin_dashboard():
    admin = Administrador.query.filter_by(id_professor=current_user.id_professor).first()

    if not admin:
        flash("Você não tem permissão para acessar esta área.", "warning")
        return redirect(url_for("area_professor.area_professor"))

    form = AdminForm()
    form_pagamento = PagamentoForm()
    form.aluno_id.choices = [(aluno.id_aluno, aluno.nome) for aluno in Aluno.query.all()]
    form.plano_id.choices = [(plano.id_plano, plano.nomePlano) for plano in Plano.query.all()]

    aluno = None
    pagamentos = []
    valor_a_pagar = None

    # Capturar o aluno selecionado
    aluno_id = request.args.get('aluno_id', type=int) or form.aluno_id.data
    print(f"Aluno ID capturado: {aluno_id}")  # Log para depuração
    if aluno_id:
        aluno = Aluno.query.get(aluno_id)
        if aluno:
            print(f"Aluno encontrado: {aluno.nome}")  # Log para depuração
            # Obter os pagamentos do aluno
            pagamentos = Pagamento.query.filter_by(id_aluno=aluno.id_aluno).all()

            # Obter o valor do plano do aluno
            if aluno.plano_id:
                plano = Plano.query.get(aluno.plano_id)
                if plano:
                    valor_a_pagar = plano.preco

    if form.validate_on_submit():
        aluno_id = form.aluno_id.data  # Capturar o aluno_id do formulário
        aluno = Aluno.query.get(aluno_id)
        if aluno:
            print(f"Atualizando dados do aluno: {aluno.nome}")  # Log para depuração

            # Atualizar os dados do aluno
            if form.nome.data.strip():
                aluno.nome = form.nome.data.strip()
            if form.email.data.strip():
                aluno.email = form.email.data.strip()
            if form.telefone.data.strip():
                aluno.telefone = form.telefone.data.strip()
            if form.cpf.data.strip():
                aluno.cpf = form.cpf.data.strip()
            if form.data_nascimento.data:
                aluno.data_nascimento = form.data_nascimento.data
            if form.plano_id.data:
                print(f"Atualizando plano do aluno para: {form.plano_id.data}")  # Log para depuração
                aluno.plano_id = form.plano_id.data  # Atualizar o plano do aluno
            aluno.status = form.status.data == "ativo"

            # Atualizar a senha, se fornecida
            if form.senha.data.strip():
                aluno.set_senha(form.senha.data.strip())

            # Atualizar os pagamentos
            for mes in ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']:
                status_pagamento = request.form.get(f"status_pagamento_{mes}")
                print(f"Status de pagamento para {mes}: {status_pagamento}")  # Log para depuração
                if status_pagamento:
                    pagamento = Pagamento.query.filter_by(id_aluno=aluno.id_aluno, mes=mes).first()
                    if not pagamento:
                        # Criar um novo registro de pagamento
                        pagamento = Pagamento(
                            id_aluno=aluno.id_aluno,
                            mes=mes,
                            status=status_pagamento  # "pago" ou "nao_pago"
                        )
                        db.session.add(pagamento)
                    else:
                        # Atualizar o status do pagamento existente
                        pagamento.status = status_pagamento

            # Salvar as alterações no banco de dados
            try:
                db.session.commit()
                print("Pagamentos atualizados com sucesso.")  # Log para depuração
                flash("Pagamentos atualizados com sucesso!", "success")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao atualizar pagamentos: {e}")  # Log para depuração
                flash("Erro ao atualizar os pagamentos.", "danger")

        return redirect(url_for('admin.admin_dashboard', aluno_id=aluno_id))

    # Atualizar pagamentos na tabela
    if request.method == "POST" and "status" in request.form:
        mes = request.form.get("mes")
        status_pagamento = request.form.get("status")
        if mes and status_pagamento:
            pagamento = Pagamento.query.filter_by(id_aluno=aluno.id_aluno, mes=mes).first()
            if not pagamento:
                pagamento = Pagamento(id_aluno=aluno.id_aluno, mes=mes, status=status_pagamento)
                db.session.add(pagamento)
            else:
                pagamento.status = status_pagamento
            try:
                db.session.commit()
                flash(f"Pagamento para {mes} atualizado com sucesso!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao atualizar pagamento para {mes}: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard', aluno_id=aluno_id))

    # Registrar pagamento manual
    if form_pagamento.validate_on_submit():
        mes = form_pagamento.mes.data
        status = form_pagamento.status.data
        pagamento = Pagamento.query.filter_by(id_aluno=aluno.id_aluno, mes=mes).first()
        if not pagamento:
            pagamento = Pagamento(id_aluno=aluno.id_aluno, mes=mes, status=status)
            db.session.add(pagamento)
        else:
            pagamento.status = status
        try:
            db.session.commit()
            flash(f"Pagamento para {mes} registrado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao registrar pagamento para {mes}: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard', aluno_id=aluno_id))

    return render_template(
        'administracao.html',
        form=form,
        form_pagamento=form_pagamento,
        admin=admin,
        aluno=aluno,
        pagamentos=pagamentos,
        valor_a_pagar=valor_a_pagar
    )
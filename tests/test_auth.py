import pytest
from decimal import Decimal

from main import create_app
from extensions import db
from models import Plano


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })

    with app.app_context():
        db.create_all()
        yield app


def test_register_aluno(app):
    client = app.test_client()

    with app.app_context():
        plano = Plano(nomePlano='Basico', preco=Decimal('99.90'))
        db.session.add(plano)
        db.session.commit()

    data = {
        'nome': 'Teste Aluno',
        'email': 'teste@example.com',
        'senha': 'senha123',
        'confirmar': 'senha123',
        'telefone': '11999999999',
        'cpf': '12345678909',
        'data_nascimento': '1990-01-01',
        'plano_id': str(plano.id_plano),
    }

    resp = client.post('/registrar/aluno/', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Aluno registrado com sucesso' in resp.data or b'Aluno registrado com sucesso!' in resp.data

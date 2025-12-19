from main import db, app
from models import Professor


def seed_professor():
    novo_professor = Professor(
        nome="João Silva",
        telefone="11987654321",
        especialidade="Musculação",
        email="joao@email.com",
    )

    # Use the model helper to set the password correctly
    novo_professor.set_senha("senha123")

    db.session.add(novo_professor)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        seed_professor()


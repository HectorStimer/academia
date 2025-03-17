from email.policy import default
from main import db
from models import Professor
from werkzeug.security import generate_password_hash

novo_professor = Professor(
    
    
    nome="João Silva",
    telefone="11987654321",
    especialidade="Musculação",
    email="joao@email.com",
    senha=generate_password_hash("senha123")  # Armazena a senha criptografada
)

db.session.add(novo_professor)
db.session.commit()


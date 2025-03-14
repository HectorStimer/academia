from main import app, db  # Certifique-se de que o db e o app estão sendo importados corretamente
from models import Plano  # Importa o modelo Plano

# Criando o plano
novo_plano = Plano(nomePlano="Mensal", preco=99.99)

# Criando o contexto da aplicação Flask
with app.app_context():
    # Adiciona o plano à sessão do banco de dados
    db.session.add(novo_plano)
    db.session.commit()

print("Plano 'Mensal' foi adicionado com sucesso!")

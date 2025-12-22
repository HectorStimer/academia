
# Academia (projeto Flask)

Aplicação de exemplo para gerenciar **alunos**, **professores**, **planos**, **pagamentos** e **progresso** — com foco em boas práticas (application factory, Blueprints, migrações, testes e CI).

---

## 🔎 O que tem neste repositório

- **`main.py`** — application factory (`create_app`) e bootstrap da aplicação
- **`config.py`** — configuração via variáveis de ambiente (dotenv)
- **`extensions.py`** — db (SQLAlchemy), LoginManager, etc.
- **`models.py`** — modelos de domínio (Aluno, Professor, Plano, Treinamento...)
- **`forms.py`** — formulários WTForms
- **`routes/`** — blueprints organizados por área (auth, areaAluno, areaProfessor, administracao...)
- **`templates/`**, **`static/`** — frontend (Jinja2 + CSS)
- **`create_db.py`**, **`create_plano.py`** — scripts utilitários (criar tabelas e seed)
- **`tests/`** — testes automatizados (pytest)
- **`Dockerfile`**, **`docker-compose.yml`** — facilitar execução local em containers
- **`requirements.txt`** — dependências Python
- **`.github/workflows/ci.yml`** — pipeline de CI (executa testes)

---

## 🧰 Tecnologias principais

- Python 3.11
- Flask (Blueprints, Application Factory)
- Flask-SQLAlchemy, Flask-Migrate
- Flask-Login, Flask-WTF (WTForms)
- MySQL (container via Docker)
- pytest, pytest-flask
- Docker & docker-compose
- GitHub Actions (CI)

---

## 🚀 Como rodar (rápido)

### Com Docker (recomendado)

1. Inicie os serviços:

```powershell
docker compose up --build -d
```

2. Aguarde o banco ficar `healthy` e execute os utilitários:

```powershell
docker compose exec web python create_db.py
docker compose exec web python create_plano.py
```

3. Acesse: `http://localhost:5000`

Observações:
- Se a porta 3306 do host estiver ocupada, o compose mapeia o MySQL para `3307:3306` por padrão.

### Local (sem Docker)

1. Crie um virtualenv e instale dependências:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure variáveis de ambiente (ex.: `SECRET_KEY`, `DATABASE_URL`). Use `.env` baseado em `.env.example`.

3. Crie DB/seed e rode a app:

```powershell
python create_db.py
python create_plano.py
python main.py
```

ou via Flask CLI:

```powershell
$env:FLASK_APP='main.py'
flask run
```

---

## ✅ Testes e CI

- Rodar testes no container:

```powershell
docker compose exec web env PYTHONPATH=/app pytest -q
```

- Local: `pytest -q`
- CI: existe um workflow do GitHub Actions que executa `pytest` em push/PR.

---

## 🔁 Migrações e seeds

- **Migrações** (Flask-Migrate):

```powershell
flask db init   # (se ainda não houver migrations)
flask db migrate -m "mensagem"
flask db upgrade
```

- **Seeds / utilitários**:

```powershell
python create_db.py   # cria tabelas (para desenvolvimento)
python create_plano.py  # insere plano/professor de exemplo
```

---

## 🐞 Troubleshooting rápido

- `email_validator` faltando: instale `email-validator` (`requirements.txt` já atualizado).
- Erro "no secret key set": defina `SECRET_KEY` no `.env` ou no cfg de testes.
- MySQL 8 auth: se houver erro de autenticação, certifique-se de ter `cryptography` instalado (já incluído nas dependências).
- Docker: verifique se o Docker daemon está rodando e aguarde a saúde do container DB (`docker compose ps` / `docker compose logs db`).

---

## 🤝 Contribuições

1. Crie uma branch a partir de `main` ou da branch de features.
2. Escreva testes para suas mudanças.
3. Abra um Pull Request e descreva as alterações detalhadamente.


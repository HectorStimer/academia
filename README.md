
# Academia Hydra — Aplicação Flask

Projeto simples para gerenciar alunos, professores, planos, pagamentos e progresso físico de uma academia, com usuarios de aluno e professor separados.

Principais tecnologias: **Flask**, **Flask-SQLAlchemy**, **Flask-Login**, **Flask-WTF**, **MySQL (opcional via Docker)**.

---

## 🚀 Quickstart

Recomendado: executar via **Docker Compose** (inicia web + banco MySQL).

### Com Docker (recomendado)

1. Subir os serviços:

```powershell
docker compose up --build -d
```

2. Aguarde o serviço `db` ficar saudável e rode os scripts de criação/seed:

```powershell
docker compose exec web python create_db.py
docker compose exec web python create_plano.py
```

3. Abra http://localhost:5000 no navegador.

> Obs: se a porta 3306 do host estiver em uso, o compose usa a porta `3307` no host por padrão.

### Sem Docker (local)

1. Instale Python 3.10+ e crie um virtualenv:

```powershell
python -m venv venv
.\venv\Scripts\pip.exe install --upgrade pip
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\python.exe main.py
```

2. Ajuste `DATABASE_URL` e `SECRET_KEY` (use `.env` ou variáveis de ambiente). Veja `.env.example`.

---

## ⚙️ Variáveis de ambiente

Coloque no `.env` (ou exporte no ambiente):

- `DATABASE_URL` — URI de conexão (ex.: `mysql+pymysql://root:example@db/academiahydra`)
- `SECRET_KEY` — chave secreta do Flask

Um exemplo está no arquivo `.env.example` no repositório.

---

## 🧱 Banco de dados / Seed

- `create_db.py` — cria as tabelas (usa `db.create_all()`)
- `create_plano.py` — script de seed para criar um usuário professor de exemplo

Execute-os dentro do container (`docker compose exec web ...`) ou localmente com o venv ativo.

---

## 📁 Estrutura do projeto (resumo)

- `main.py` — instancia app, registra blueprints e configura LoginManager
- `models.py` — modelos SQLAlchemy
- `forms.py` — formulários WTForms
- `routes/` — blueprints por área (login, admin, aluno, professor, pagamentos)
- `templates/` e `static/` — front-end
- `extensions.py` — inicialização de `db` e `LoginManager`

---

## Boas práticas / notas e recomendações

- **Segurança**: não comitar segredos. Use `.env` e `.gitignore` (já adicionado). 🔒
- **App factory**: considerar migrar para o padrão application factory para testes e flexibilidade. 🧩
- **Migrations**: para produção, adicionar Alembic (Flask-Migrate) para versionamento do esquema do DB. 🗂️
- **Testes**: adicionar testes automatizados (pytest) e CI (GitHub Actions) para cobertura básica. 🧪

---

## 🧩 Contribuindo

1. Abra uma issue ou PR descrevendo a mudança.
2. Faça uma branch, escreva testes e inclua passos de reprodução no PR.

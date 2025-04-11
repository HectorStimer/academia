from flask import Flask
from config import Config
from extensions import db, lm

# Importar Blueprints
from routes.administracao import admin_bp
from routes.areaProfessor import area_professor_bp
from routes.areaAluno import areaAluno_bp
from routes.homepage import homepage_bp
from routes.loginAluno import login_aluno_bp
from routes.loginProfessor import login_professor_bp
from routes.logout import logout_bp
from routes.pagamentos import pagamentos_bp
from routes.registrarProfessor import registrar_professor_bp
from routes.registrarAluno import registrar_aluno_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
lm.init_app(app)

# Registrar Blueprints
app.register_blueprint(admin_bp, url_prefix="/administracao")
app.register_blueprint(area_professor_bp, url_prefix="/area/professor")
app.register_blueprint(areaAluno_bp, url_prefix="/area/aluno")
app.register_blueprint(homepage_bp, url_prefix="/")
app.register_blueprint(login_aluno_bp, url_prefix="/login/aluno")
app.register_blueprint(login_professor_bp, url_prefix="/login/professor")
app.register_blueprint(logout_bp, url_prefix="/logout")
app.register_blueprint(pagamentos_bp, url_prefix="/pagamentos")
app.register_blueprint(registrar_professor_bp, url_prefix="/registrar/professor")
app.register_blueprint(registrar_aluno_bp, url_prefix="/registrar/aluno")

# Função user_loader para carregar o usuário
@lm.user_loader
def user_loader(user_id):
    from models import Aluno, Professor
    aluno = Aluno.query.get(user_id)
    if aluno:
        return aluno

    professor = Professor.query.get(user_id)
    if professor:
        return professor

    return None


if __name__ == "__main__":
    app.run(debug=True)

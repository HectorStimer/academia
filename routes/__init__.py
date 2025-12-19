"""Routes package - exposes blueprints to be registered by the application."""

from .administracao import admin_bp
from .areaAluno import areaAluno_bp
from .areaProfessor import area_professor_bp
from .homepage import homepage_bp
from .loginAluno import login_aluno_bp
from .loginProfessor import login_professor_bp
from .logout import logout_bp
from .pagamentos import pagamentos_bp
from .registrarProfessor import registrar_professor_bp
from .registrarAluno import registrar_aluno_bp
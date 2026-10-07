from flask import Flask
from db.db_connection import db

from dotenv import load_dotenv
import os

from model.pessoa import Pessoa
from model.aluno import Aluno
from model.professor import Professor
from model.graduacao import Graduacao
from model.trilha import Trilha
from model.curso import Curso
from model.conteudo import Conteudo
from model.inscricao import Inscricao
from model.professor_graduacao import ProfessorGraduacao
from model.graduacao_trilha import GraduacaoTrilha
from model.professor_curso import ProfessorCurso

from controller.aluno_controller import aluno_bp
from controller.conteudo_controller import conteudo_bp
from controller.curso_controller import curso_bp
from controller.graduacao_controller import graduacao_bp
from controller.inscricao_controller import inscricao_bp
from controller.professor_controller import professor_bp
from controller.trilha_controller import trilha_bp

load_dotenv()

app = Flask(__name__)

db_usuario = os.getenv("DB_USUARIO")
db_senha = os.getenv("DB_SENHA")
db_host = os.getenv("DB_HOST")
db_porta = os.getenv("DB_PORTA")
db_banco = os.getenv("DB_BANCO")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg://{db_usuario}:{db_senha}"
    f"@{db_host}:{db_porta}/{db_banco}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(aluno_bp)
app.register_blueprint(conteudo_bp)
app.register_blueprint(curso_bp)
app.register_blueprint(graduacao_bp)
app.register_blueprint(inscricao_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(trilha_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
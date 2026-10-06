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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
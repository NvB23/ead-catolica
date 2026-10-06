from db.db_connection import db
from model.aluno import Aluno

class AlunoDAO:

    @staticmethod
    def salvar(aluno):
        try:
            db.session.add(aluno)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def editar(aluno, nome, email, senha, graduacao):
        try:
            aluno.nome = nome
            aluno.email = email
            aluno.senha = senha
            aluno.graduacao = graduacao

            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def remover(aluno):
        try:
            db.session.delete(aluno)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def listar_todos():
        return Aluno.query.all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Aluno, id)

    @staticmethod
    def buscar_por_nome(nome):
        return Aluno.query.filter(
            Aluno.nome.ilike(f"%{nome}%")
        ).all()
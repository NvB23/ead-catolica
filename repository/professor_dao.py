from db.db_connection import db
from model.professor import Professor

class ProfessorDAO:

    @staticmethod
    def salvar(professor):
        try:
            db.session.add(professor)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def editar(professor, nome, email, senha, sobre, formacoes, graduacoes, cursos):
        try:
            professor.nome = nome
            professor.email = email
            professor.senha = senha
            professor.sobre = sobre
            professor.formacoes = formacoes
            professor.graduacoes = graduacoes
            professor.cursos = cursos

            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def remover(professor):
        try:
            db.session.delete(professor)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def listar_todos():
        return Professor.query.all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Professor, id)

    @staticmethod
    def buscar_por_nome(nome):
        return Professor.query.filter(
            Professor.nome.ilike(f"%{nome}%")
        ).all()
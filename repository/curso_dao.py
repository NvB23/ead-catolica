from db.db_connection import db
from model.curso import Curso

class CursoDAO:

    @staticmethod
    def salvar(curso):
        try:
            db.session.add(curso)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def editar(curso, nome, descricao, capa, trilha, professores):
        try:
            curso.nome = nome
            curso.descricao = descricao
            curso.capa = capa
            curso.trilha = trilha
            curso.professores = professores

            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def remover(curso):
        try:
            db.session.delete(curso)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def listar_todos():
        return Curso.query.all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Curso, id)

    @staticmethod
    def buscar_por_nome(nome):
        return Curso.query.filter(
            Curso.nome.ilike(f"%{nome}%")
        ).all()
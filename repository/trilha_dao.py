from db.db_connection import db
from model.trilha import Trilha

class TrilhaDAO:

    @staticmethod
    def salvar(trilha):
        try:
            db.session.add(trilha)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def editar(trilha, nome, graduacoes):
        try:
            trilha.nome = nome
            trilha.graduacoes = graduacoes

            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def remover(trilha):
        try:
            db.session.delete(trilha)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def listar_todos():
        return Trilha.query.all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Trilha, id)

    @staticmethod
    def buscar_por_nome(nome):
        return Trilha.query.filter(
            Trilha.nome.ilike(f"%{nome}%")
        ).all()
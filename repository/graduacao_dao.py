from db.db_connection import db
from model.graduacao import Graduacao

class GraduacaoDAO:

    @staticmethod
    def salvar(graduacao):
        try:
            db.session.add(graduacao)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def editar(graduacao, nome, professores, trilhas):
        try:
            graduacao.nome = nome
            graduacao.professores = professores
            graduacao.trilhas = trilhas

            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def remover(graduacao):
        try:
            db.session.delete(graduacao)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def listar_todos():
        return Graduacao.query.all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Graduacao, id)

    @staticmethod
    def buscar_por_nome(nome):
        return Graduacao.query.filter(
            Graduacao.nome.ilike(f"%{nome}%")
        ).all()
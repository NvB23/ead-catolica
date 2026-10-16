from db.db_connection import db
from model.pessoa import Pessoa


class PessoaDAO:

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Pessoa, id)

    @staticmethod
    def buscar_por_email(email):
        for pessoa in Pessoa.query.all():
            if pessoa.email.lower() == email.lower():
                return pessoa
        return None

    @staticmethod
    def atualizar_senha(pessoa, senha):
        try:
            pessoa.senha = senha
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

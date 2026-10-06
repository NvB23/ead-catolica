from db.db_connection import db
from model.inscricao import Inscricao

class InscricaoDAO:

    @staticmethod
    def salvar(inscricao):
        try:
            db.session.add(inscricao)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def editar(inscricao, progresso, concluido, data_conclusao):
        try:
            inscricao.progresso = progresso
            inscricao.concluido = concluido
            inscricao.data_conclusao = data_conclusao

            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def remover(inscricao):
        try:
            db.session.delete(inscricao)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def listar_todos():
        return Inscricao.query.all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Inscricao, id)

    @staticmethod
    def buscar_por_aluno(aluno_id):
        return Inscricao.query.filter_by(
            aluno_id=aluno_id
        ).all()

    @staticmethod
    def buscar_por_curso(curso_id):
        return Inscricao.query.filter_by(
            curso_id=curso_id
        ).all()

    @staticmethod
    def buscar_por_aluno_e_curso(aluno_id, curso_id):
        return Inscricao.query.filter_by(
            aluno_id=aluno_id,
            curso_id=curso_id
        ).first()
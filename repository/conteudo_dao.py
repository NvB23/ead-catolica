from db.db_connection import db
from model.conteudo import Conteudo

class ConteudoDAO:

    @staticmethod
    def salvar(conteudo):
        try:
            db.session.add(conteudo)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def editar(conteudo, nome, descricao, curso, tipo, ordem, capa, texto, url):
        try:
            conteudo.nome = nome
            conteudo.descricao = descricao
            conteudo.curso = curso
            conteudo.tipo = tipo
            conteudo.ordem = ordem
            conteudo.capa = capa
            conteudo.texto = texto
            conteudo.url = url

            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def remover(conteudo):
        try:
            db.session.delete(conteudo)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def listar_todos():
        return Conteudo.query.order_by(
            Conteudo.ordem
        ).all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Conteudo, id)

    @staticmethod
    def buscar_por_nome(nome):
        return Conteudo.query.filter(
            Conteudo.nome.ilike(f"%{nome}%")
        ).all()
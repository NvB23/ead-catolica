from db.db_connection import db
from model.tipo_conteudo import TipoConteudo

class Conteudo(db.Model):
    __tablename__ = "conteudo"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    descricao = db.Column(
        db.Text,
        nullable=True
    )

    curso_id = db.Column(
        db.Integer,
        db.ForeignKey("curso.id"),
        nullable=False
    )

    tipo = db.Column(
        db.Enum(TipoConteudo),
        nullable=False
    )

    ordem = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    capa = db.Column(
        db.String(500),
        nullable=True
    )

    texto = db.Column(
        db.Text,
        nullable=True
    )

    url = db.Column(
        db.String(500),
        nullable=True
    )

    curso = db.relationship(
        "Curso",
        back_populates="conteudos"
    )
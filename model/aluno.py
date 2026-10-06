from db.db_connection import db
from model.pessoa import Pessoa

class Aluno(Pessoa):
    __tablename__ = "aluno"

    id = db.Column(
        db.Integer,
        db.ForeignKey("pessoa.id"),
        primary_key=True
    )

    graduacao_id = db.Column(
        db.Integer,
        db.ForeignKey("graduacao.id"),
        nullable=False
    )

    graduacao = db.relationship(
        "Graduacao",
        back_populates="alunos"
    )

    inscricoes = db.relationship(
        "Inscricao",
        back_populates="aluno",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "aluno"
    }
from datetime import datetime
from db.db_connection import db

class Inscricao(db.Model):
    __tablename__ = "inscricao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey("aluno.id"),
        nullable=False
    )

    curso_id = db.Column(
        db.Integer,
        db.ForeignKey("curso.id"),
        nullable=False
    )

    progresso = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    concluido = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    data_inicio = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now
    )

    data_conclusao = db.Column(
        db.DateTime,
        nullable=True
    )

    aluno = db.relationship(
        "Aluno",
        back_populates="inscricoes"
    )

    curso = db.relationship(
        "Curso",
        back_populates="inscricoes"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "aluno_id",
            "curso_id",
            name="uq_aluno_curso"
        ),
    )
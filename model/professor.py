from db.db_connection import db
from model.pessoa import Pessoa

class Professor(Pessoa):
    __tablename__ = "professor"

    id = db.Column(
        db.Integer,
        db.ForeignKey("pessoa.id"),
        primary_key=True
    )

    sobre = db.Column(
        db.Text,
        nullable=True
    )

    formacoes = db.Column(
        db.Text,
        nullable=True
    )

    graduacoes = db.relationship(
        "Graduacao",
        secondary="professor_graduacao",
        back_populates="professores"
    )

    cursos = db.relationship(
        "Curso",
        secondary="professor_curso",
        back_populates="professores"
    )

    __mapper_args__ = {
        "polymorphic_identity": "professor"
    }
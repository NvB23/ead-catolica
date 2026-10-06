from db.db_connection import db

class Graduacao(db.Model):
    __tablename__ = "graduacao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    alunos = db.relationship(
        "Aluno",
        back_populates="graduacao"
    )

    professores = db.relationship(
        "Professor",
        secondary="professor_graduacao",
        back_populates="graduacoes"
    )

    trilhas = db.relationship(
        "Trilha",
        secondary="graduacao_trilha",
        back_populates="graduacoes"
    )
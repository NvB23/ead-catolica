from db.db_connection import db

class Trilha(db.Model):
    __tablename__ = "trilha"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    graduacoes = db.relationship(
        "Graduacao",
        secondary="graduacao_trilha",
        back_populates="trilhas"
    )

    cursos = db.relationship(
        "Curso",
        back_populates="trilha",
        cascade="all, delete-orphan"
    )
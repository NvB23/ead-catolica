from db.db_connection import db

class Curso(db.Model):
    __tablename__ = "curso"

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

    capa = db.Column(
        db.String(500),
        nullable=True
    )

    trilha_id = db.Column(
        db.Integer,
        db.ForeignKey("trilha.id"),
        nullable=False
    )

    trilha = db.relationship(
        "Trilha",
        back_populates="cursos"
    )

    conteudos = db.relationship(
        "Conteudo",
        back_populates="curso",
        cascade="all, delete-orphan",
        order_by="Conteudo.ordem"
    )

    professores = db.relationship(
        "Professor",
        secondary="professor_curso",
        back_populates="cursos"
    )
from db.db_connection import db

class Pessoa(db.Model):
    __tablename__ = "pessoa"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "pessoa"
    }
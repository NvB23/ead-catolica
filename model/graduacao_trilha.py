from db.db_connection import db


class GraduacaoTrilha(db.Model):
    __tablename__ = "graduacao_trilha"

    graduacao_id = db.Column(
        db.Integer,
        db.ForeignKey("graduacao.id"),
        primary_key=True
    )

    trilha_id = db.Column(
        db.Integer,
        db.ForeignKey("trilha.id"),
        primary_key=True
    )
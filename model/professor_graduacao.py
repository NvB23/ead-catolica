from db.db_connection import db


class ProfessorGraduacao(db.Model):
    __tablename__ = "professor_graduacao"

    professor_id = db.Column(
        db.Integer,
        db.ForeignKey("professor.id"),
        primary_key=True
    )

    graduacao_id = db.Column(
        db.Integer,
        db.ForeignKey("graduacao.id"),
        primary_key=True
    )
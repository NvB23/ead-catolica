from db.db_connection import db

class ProfessorCurso(db.Model):
    __tablename__ = "professor_curso"

    professor_id = db.Column(
        db.Integer,
        db.ForeignKey("professor.id"),
        primary_key=True
    )

    curso_id = db.Column(
        db.Integer,
        db.ForeignKey("curso.id"),
        primary_key=True
    )
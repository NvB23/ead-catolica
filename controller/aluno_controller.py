from flask import Blueprint

aluno_bp = Blueprint("aluno", __name__, url_prefix="/aluno")

@aluno_bp.route("/", methods=["GET"])
def teste():
    return "Teste"
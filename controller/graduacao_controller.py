from flask import Blueprint, jsonify, abort
from db.dados_iniciais import listar_graduacoes_fixas

graduacao_bp = Blueprint("graduacao", __name__, url_prefix="/graduacao")


@graduacao_bp.route("/", methods=["POST"], strict_slashes=False)
@graduacao_bp.route("/<int:id>", methods=["PUT", "DELETE"])
def bloquear_alteracao(id=None):
    abort(403, description="As graduações já são definidas no banco e não podem ser alteradas por alunos ou professores.")


@graduacao_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    lista = []
    for graduacao in listar_graduacoes_fixas():
        lista.append({"id": graduacao.id, "nome": graduacao.nome})
    return jsonify(lista)


@graduacao_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    for graduacao in listar_graduacoes_fixas():
        if graduacao.id == id:
            return jsonify({"id": graduacao.id, "nome": graduacao.nome})
    abort(404, description="Graduação não encontrada.")


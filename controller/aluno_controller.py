from flask import Blueprint, jsonify, g, abort, request
from service.aluno_service import AlunoService
from service.acesso_service import AcessoService
from controller.auxiliar import ler_dados, responder

aluno_bp = Blueprint("aluno", __name__, url_prefix="/aluno")


@aluno_bp.route("/", methods=["POST"], strict_slashes=False)
def bloquear_cadastro():
    abort(403, description="O cadastro de aluno é realizado na página de cadastro.")


def converter(aluno):
    return {"id": aluno.id, "nome": aluno.nome, "email": aluno.email,
            "graduacao_id": aluno.graduacao_id, "graduacao": aluno.graduacao.nome}


def listar_permitidos():
    if g.usuario.tipo == "aluno":
        return [g.usuario]
    lista = []
    for inscricao in AcessoService.listar_inscricoes(g.usuario):
        if inscricao.aluno not in lista:
            lista.append(inscricao.aluno)
    return lista


@aluno_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    lista = []
    for aluno in listar_permitidos():
        lista.append(converter(aluno))
    return jsonify(lista)


@aluno_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    for aluno in listar_permitidos():
        if aluno.id == id:
            return jsonify(converter(aluno))
    abort(403, description="Você não tem acesso a este aluno.")


@aluno_bp.route("/<int:id>", methods=["PUT"])
@aluno_bp.route("/<int:id>/editar", methods=["POST"])
def editar(id):
    if g.usuario.tipo != "aluno" or g.usuario.id != id:
        abort(403, description="Você só pode editar o seu perfil.")
    dados = ler_dados()
    if dados.get("graduacao_id", g.usuario.graduacao_id) != g.usuario.graduacao_id:
        abort(403, description="A graduação do cadastro não pode ser alterada por esta rota.")
    if AlunoService.editar(id, dados.get("nome"), dados.get("email"), dados.get("senha"), g.usuario.graduacao_id):
        if request.is_json:
            return jsonify(converter(g.usuario))
        return responder("Perfil atualizado.", "perfil")
    return responder("Não foi possível atualizar o perfil.", "perfil", 500)


from flask import Blueprint, jsonify, g, abort
from service.inscricao_service import InscricaoService
from service.acesso_service import AcessoService
from controller.curso_controller import obter_curso
from controller.auxiliar import ler_dados, responder

inscricao_bp = Blueprint("inscricao", __name__, url_prefix="/inscricao")


def converter(inscricao):
    return {"id": inscricao.id, "aluno_id": inscricao.aluno_id, "curso_id": inscricao.curso_id}


def obter_inscricao(id, editar=False):
    inscricao = InscricaoService.buscar_por_id(id)
    if inscricao is None:
        abort(404, description="Inscrição não encontrada.")
    if not AcessoService.pode_ver_inscricao(g.usuario, inscricao):
        abort(403, description="Você não tem acesso a esta inscrição.")
    if editar and (g.usuario.tipo != "aluno" or inscricao.aluno_id != g.usuario.id):
        abort(403, description="O aluno só pode alterar a própria inscrição.")
    return inscricao


@inscricao_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    lista = []
    for inscricao in AcessoService.listar_inscricoes(g.usuario):
        lista.append(converter(inscricao))
    return jsonify(lista)


@inscricao_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    return jsonify(converter(obter_inscricao(id)))


@inscricao_bp.route("/", methods=["POST"], strict_slashes=False)
def salvar():
    if g.usuario.tipo != "aluno":
        abort(403, description="A inscrição é feita pelo próprio aluno.")
    dados = ler_dados()
    if dados.get("aluno_id", g.usuario.id) != g.usuario.id:
        abort(403, description="Você só pode inscrever a sua conta.")
    curso = obter_curso(dados.get("curso_id"))
    if InscricaoService.salvar(g.usuario.id, curso.id):
        return responder("Inscrição realizada.", "inscricao", 201)
    return responder("Não foi possível realizar a inscrição.", "inscricao", 500)


@inscricao_bp.route("/<int:id>", methods=["PUT"])
@inscricao_bp.route("/<int:id>/editar", methods=["POST"])
def editar(id):
    obter_inscricao(id, editar=True)
    abort(403, description="A atualização de progresso está desativada.")


@inscricao_bp.route("/<int:id>", methods=["DELETE"])
@inscricao_bp.route("/<int:id>/remover", methods=["POST"])
def remover(id):
    obter_inscricao(id, editar=True)
    if InscricaoService.remover(id):
        return responder("Inscrição cancelada.", "inscricao")
    return responder("Não foi possível cancelar a inscrição.", "inscricao", 500)


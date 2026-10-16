from flask import Blueprint, jsonify, g, request, abort
from service.trilha_service import TrilhaService
from service.acesso_service import AcessoService
from controller.auth_controller import professor_obrigatorio
from controller.auxiliar import ler_dados, responder

trilha_bp = Blueprint("trilha", __name__, url_prefix="/trilha")


def converter(trilha):
    graduacoes = []
    for graduacao in trilha.graduacoes:
        graduacoes.append({"id": graduacao.id, "nome": graduacao.nome})
    return {"id": trilha.id, "nome": trilha.nome, "graduacoes": graduacoes}


def obter_trilha(id, editar=False):
    trilha = TrilhaService.buscar_por_id(id)
    if trilha is None:
        abort(404, description="Trilha não encontrada.")
    if editar:
        permitido = AcessoService.pode_gerenciar_trilha(g.usuario, trilha)
    else:
        permitido = trilha in AcessoService.listar_trilhas(g.usuario)
    if not permitido:
        abort(403, description="Você não pode alterar ou acessar esta trilha.")
    return trilha


@trilha_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    lista = []
    for trilha in AcessoService.listar_trilhas(g.usuario):
        lista.append(converter(trilha))
    return jsonify(lista)


@trilha_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    return jsonify(converter(obter_trilha(id)))


@trilha_bp.route("/", methods=["POST"], strict_slashes=False)
@professor_obrigatorio
def salvar():
    dados = ler_dados()
    AcessoService.validar_graduacoes_professor(g.usuario, dados.get("graduacao_ids"))
    if TrilhaService.salvar(dados.get("nome"), dados.get("graduacao_ids")):
        return responder("Trilha cadastrada.", "trilha", 201)
    return responder("Não foi possível cadastrar a trilha.", "trilha", 500)


@trilha_bp.route("/<int:id>", methods=["PUT"])
@trilha_bp.route("/<int:id>/editar", methods=["POST"])
@professor_obrigatorio
def editar(id):
    trilha = obter_trilha(id, editar=True)
    dados = ler_dados()
    AcessoService.validar_graduacoes_professor(g.usuario, dados.get("graduacao_ids"))
    if trilha.cursos:
        ids_atuais = []
        for graduacao in trilha.graduacoes:
            ids_atuais.append(graduacao.id)
        if set(ids_atuais) != set(dados.get("graduacao_ids")):
            raise ValueError("Uma trilha com cursos mantém as graduações atuais.")
    if TrilhaService.editar(id, dados.get("nome"), dados.get("graduacao_ids")):
        if request.is_json:
            return jsonify(converter(trilha))
        return responder("Trilha atualizada.", "trilha")
    return responder("Não foi possível editar a trilha.", "trilha", 500)


@trilha_bp.route("/<int:id>", methods=["DELETE"])
@trilha_bp.route("/<int:id>/remover", methods=["POST"])
@professor_obrigatorio
def remover(id):
    obter_trilha(id, editar=True)
    if TrilhaService.remover(id):
        return responder("Trilha excluída.", "trilha")
    return responder("Não foi possível excluir a trilha.", "trilha", 500)


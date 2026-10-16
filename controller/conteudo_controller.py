from flask import Blueprint, jsonify, request, g, abort
from service.conteudo_service import ConteudoService
from service.acesso_service import AcessoService
from controller.curso_controller import obter_curso
from controller.auth_controller import professor_obrigatorio
from controller.auxiliar import ler_dados, responder

conteudo_bp = Blueprint("conteudo", __name__, url_prefix="/conteudo")


def converter(conteudo):
    return {"id": conteudo.id, "nome": conteudo.nome, "descricao": conteudo.descricao,
            "curso_id": conteudo.curso_id, "tipo": conteudo.tipo.value,
            "ordem": conteudo.ordem, "texto": conteudo.texto, "url": conteudo.url}


def obter_conteudo(id, editar=False):
    conteudo = ConteudoService.buscar_por_id(id)
    if conteudo is None:
        abort(404, description="Aula não encontrada.")
    obter_curso(conteudo.curso_id, editar=editar, aulas=not editar)
    return conteudo


@conteudo_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    lista = []
    for conteudo in ConteudoService.listar_todos():
        if AcessoService.pode_ver_aulas(g.usuario, conteudo.curso):
            lista.append(converter(conteudo))
    return jsonify(lista)


@conteudo_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    return jsonify(converter(obter_conteudo(id)))


@conteudo_bp.route("/", methods=["POST"], strict_slashes=False)
@professor_obrigatorio
def salvar():
    dados = ler_dados()
    curso = obter_curso(dados.get("curso_id"), editar=True)
    if ConteudoService.salvar(dados.get("nome"), dados.get("descricao"), curso.id, dados.get("tipo"),
                              dados.get("ordem", 0), dados.get("capa"), dados.get("texto"), dados.get("url")):
        return responder("Aula cadastrada.", "conteudo", 201)
    return responder("Não foi possível cadastrar a aula.", "conteudo", 500)


@conteudo_bp.route("/<int:id>", methods=["PUT"])
@conteudo_bp.route("/<int:id>/editar", methods=["POST"])
@professor_obrigatorio
def editar(id):
    conteudo = obter_conteudo(id, editar=True)
    dados = ler_dados()
    curso = obter_curso(dados.get("curso_id"), editar=True)
    if ConteudoService.editar(id, dados.get("nome"), dados.get("descricao"), curso.id, dados.get("tipo"),
                              dados.get("ordem", 0), conteudo.capa, dados.get("texto"), dados.get("url")):
        if request.is_json:
            return jsonify(converter(conteudo))
        return responder("Aula atualizada.", "conteudo")
    return responder("Não foi possível editar a aula.", "conteudo", 500)


@conteudo_bp.route("/<int:id>", methods=["DELETE"])
@conteudo_bp.route("/<int:id>/remover", methods=["POST"])
@professor_obrigatorio
def remover(id):
    conteudo = obter_conteudo(id, editar=True)
    curso_id = conteudo.curso_id
    if ConteudoService.remover(id):
        return responder("Aula excluída.", "conteudo", curso_id=curso_id)
    return responder("Não foi possível excluir a aula.", "conteudo", 500)


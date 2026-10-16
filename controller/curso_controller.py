from flask import Blueprint, jsonify, request, g, abort
from service.curso_service import CursoService
from service.trilha_service import TrilhaService
from service.acesso_service import AcessoService
from controller.auth_controller import professor_obrigatorio
from controller.auxiliar import ler_dados, responder

curso_bp = Blueprint("curso", __name__, url_prefix="/curso")


def converter(curso):
    professores = []
    for professor in curso.professores:
        professores.append({"id": professor.id, "nome": professor.nome})
    return {"id": curso.id, "nome": curso.nome, "descricao": curso.descricao,
            "trilha_id": curso.trilha_id, "professores": professores}


def obter_curso(id, editar=False, aulas=False):
    if type(id) != int:
        raise ValueError("Selecione um curso válido.")
    curso = CursoService.buscar_por_id(id)
    if curso is None:
        abort(404, description="Curso não encontrado.")
    permitido = AcessoService.pode_ver_curso(g.usuario, curso)
    if editar:
        permitido = AcessoService.pode_editar_curso(g.usuario, curso)
    if aulas:
        permitido = AcessoService.pode_ver_aulas(g.usuario, curso)
    if not permitido:
        abort(403, description="Você não tem acesso a este curso.")
    return curso


def obter_trilha(id):
    if type(id) != int:
        raise ValueError("Selecione uma trilha válida.")
    trilha = TrilhaService.buscar_por_id(id)
    if trilha is None:
        raise ValueError("Trilha não encontrada.")
    if not AcessoService.pode_usar_trilha(g.usuario, trilha):
        abort(403, description="Escolha uma trilha das suas graduações.")
    return trilha


@curso_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    lista = []
    nome = request.args.get("nome", "").lower()
    for curso in AcessoService.listar_cursos(g.usuario):
        if nome in curso.nome.lower():
            lista.append(converter(curso))
    return jsonify(lista)


@curso_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    return jsonify(converter(obter_curso(id)))


@curso_bp.route("/", methods=["POST"], strict_slashes=False)
@professor_obrigatorio
def salvar():
    dados = ler_dados()
    trilha = obter_trilha(dados.get("trilha_id"))
    if CursoService.salvar(dados.get("nome"), dados.get("descricao"), dados.get("capa"), trilha.id, [g.usuario.id]):
        return responder("Curso cadastrado.", "curso", 201)
    return responder("Não foi possível cadastrar o curso.", "curso", 500)


@curso_bp.route("/<int:id>", methods=["PUT"])
@curso_bp.route("/<int:id>/editar", methods=["POST"])
@professor_obrigatorio
def editar(id):
    curso = obter_curso(id, editar=True)
    dados = ler_dados()
    trilha = obter_trilha(dados.get("trilha_id"))
    if curso.inscricoes and trilha.id != curso.trilha_id:
        raise ValueError("Não é possível mudar a trilha de um curso com alunos inscritos.")
    professores = []
    for professor in curso.professores:
        professores.append(professor.id)
    if CursoService.editar(id, dados.get("nome"), dados.get("descricao"), curso.capa, trilha.id, professores):
        if request.is_json:
            return jsonify(converter(curso))
        return responder("Curso atualizado.", "curso")
    return responder("Não foi possível editar o curso.", "curso", 500)


@curso_bp.route("/<int:id>", methods=["DELETE"])
@curso_bp.route("/<int:id>/remover", methods=["POST"])
@professor_obrigatorio
def remover(id):
    obter_curso(id, editar=True)
    if CursoService.remover(id):
        return responder("Curso excluído.", "curso")
    return responder("Não foi possível excluir o curso.", "curso", 500)


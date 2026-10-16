from flask import Blueprint, jsonify, g, request, abort
from service.professor_service import ProfessorService
from controller.auth_controller import professor_obrigatorio
from controller.auxiliar import ler_dados, responder

professor_bp = Blueprint("professor", __name__, url_prefix="/professor")


@professor_bp.route("/", methods=["POST"], strict_slashes=False)
def bloquear_cadastro():
    abort(403, description="Professores são cadastrados previamente pelo terminal.")


def converter(professor):
    graduacoes = []
    for graduacao in professor.graduacoes:
        graduacoes.append({"id": graduacao.id, "nome": graduacao.nome})
    return {"id": professor.id, "nome": professor.nome, "email": professor.email,
            "sobre": professor.sobre, "formacoes": professor.formacoes, "graduacoes": graduacoes}


@professor_bp.route("/", methods=["GET"], strict_slashes=False)
@professor_obrigatorio
def listar():
    return jsonify([converter(g.usuario)])


@professor_bp.route("/<int:id>", methods=["GET"])
@professor_obrigatorio
def buscar(id):
    if id != g.usuario.id:
        abort(403, description="Você só pode acessar o seu perfil.")
    return jsonify(converter(g.usuario))


@professor_bp.route("/<int:id>", methods=["PUT"])
@professor_bp.route("/<int:id>/editar", methods=["POST"])
@professor_obrigatorio
def editar(id):
    if id != g.usuario.id:
        abort(403, description="Você só pode editar o seu perfil.")
    dados = ler_dados()
    graduacoes = []
    for graduacao in g.usuario.graduacoes:
        graduacoes.append(graduacao.id)
    cursos = []
    for curso in g.usuario.cursos:
        cursos.append(curso.id)
    if ProfessorService.editar(id, dados.get("nome"), dados.get("email"), dados.get("senha"),
                               dados.get("sobre"), dados.get("formacoes"), graduacoes, cursos):
        if request.is_json:
            return jsonify(converter(g.usuario))
        return responder("Perfil atualizado.", "perfil")
    return responder("Não foi possível atualizar o perfil.", "perfil", 500)


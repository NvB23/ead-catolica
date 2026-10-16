from functools import wraps
import secrets
from flask import Blueprint, request, session, g, redirect, url_for, render_template, jsonify, abort
from repository.pessoa_dao import PessoaDAO
from service.auth_service import AuthService
from service.aluno_service import AlunoService
from db.dados_iniciais import listar_graduacoes_fixas
from controller.auxiliar import ler_dados

auth_bp = Blueprint("auth", __name__)


@auth_bp.before_app_request
def carregar_usuario():
    g.usuario = None
    usuario_id = session.get("usuario_id")
    if type(usuario_id) == int:
        g.usuario = PessoaDAO.buscar_por_id(usuario_id)
    if g.usuario is not None and g.usuario.tipo not in ("aluno", "professor"):
        g.usuario = None
    if g.usuario is None and usuario_id is not None:
        session.clear()
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(24)

    publico = request.endpoint in ("auth.login", "auth.cadastro", "static", None)
    if not publico and g.usuario is None:
        if request.blueprint == "pagina":
            return redirect(url_for("auth.login"))
        return jsonify({"mensagem": "Faça login para continuar."}), 401

    if request.method in ("POST", "PUT", "DELETE") and not request.is_json:
        if request.mimetype in ("application/x-www-form-urlencoded", "multipart/form-data"):
            if request.form.get("csrf_token") != session["csrf_token"]:
                abort(400, description="Formulário expirado. Recarregue a página.")


def professor_obrigatorio(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if g.usuario is None or g.usuario.tipo != "professor":
            abort(403, description="Esta função é exclusiva do professor.")
        return funcao(*args, **kwargs)
    return verificar


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if g.usuario is not None:
            return redirect(url_for("pagina.inicio"))
        return render_template("login.html", erro=None, dados={})
    dados = ler_dados()
    try:
        pessoa = AuthService.autenticar(dados.get("email"), dados.get("senha"))
    except ValueError as erro:
        if request.is_json:
            return jsonify({"mensagem": str(erro)}), 400
        return render_template("login.html", erro=str(erro), dados=dados), 400
    if pessoa is None:
        if request.is_json:
            return jsonify({"mensagem": "E-mail ou senha incorretos."}), 401
        return render_template("login.html", erro="E-mail ou senha incorretos.", dados=dados), 401
    session.clear()
    session["usuario_id"] = pessoa.id
    session["csrf_token"] = secrets.token_urlsafe(24)
    if request.is_json:
        return jsonify({"id": pessoa.id, "nome": pessoa.nome, "perfil": pessoa.tipo})
    return redirect(url_for("pagina.inicio"), code=303)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    graduacoes = listar_graduacoes_fixas()
    if request.method == "GET":
        if request.args.get("formato") == "json":
            lista = []
            for graduacao in graduacoes:
                lista.append({"id": graduacao.id, "nome": graduacao.nome})
            return jsonify(lista)
        return render_template("cadastro.html", erro=None, dados={}, graduacoes=graduacoes)
    dados = ler_dados()
    try:
        graduacao_id = dados.get("graduacao_id")
        permitida = False
        for graduacao in graduacoes:
            if graduacao.id == graduacao_id:
                permitida = True
        if not permitida:
            raise ValueError("Selecione uma das graduações disponíveis.")

        if not AlunoService.salvar(dados.get("nome"), dados.get("email"), dados.get("senha"), graduacao_id):
            raise ValueError("Não foi possível concluir o cadastro.")
    except ValueError as erro:
        if request.is_json:
            return jsonify({"mensagem": str(erro)}), 400
        return render_template("cadastro.html", erro=str(erro), dados=dados, graduacoes=graduacoes), 400
    if request.is_json:
        return jsonify({"mensagem": "Aluno cadastrado. Faça login para continuar."}), 201
    return redirect(url_for("auth.login"), code=303)


@auth_bp.route("/sair", methods=["POST"])
def sair():
    session.clear()
    if request.is_json:
        return jsonify({"mensagem": "Sessão encerrada."})
    return redirect(url_for("auth.login"), code=303)


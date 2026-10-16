import os
from flask import Blueprint, render_template, request, redirect, url_for, g, abort, send_from_directory, current_app
from service.acesso_service import AcessoService
from service.conteudo_service import ConteudoService
from service.material_service import MaterialService
from controller.curso_controller import obter_curso
from controller.conteudo_controller import obter_conteudo
from controller.trilha_controller import obter_trilha
from controller.auth_controller import professor_obrigatorio

pagina_bp = Blueprint("pagina", __name__)


@pagina_bp.app_context_processor
def recursos_de_material():
    return {"material_da_aula": MaterialService.preparar}


def enviar_material(caminho):
    extensao = os.path.splitext(caminho)[1].lower()
    tipos_inline = (".mp4", ".webm", ".ogg", ".ogv", ".m4v", ".mp3", ".wav", ".m4a",
                    ".aac", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".pdf", ".txt")
    resposta = send_from_directory(os.path.join(current_app.root_path, "bucket"), caminho,
                                   conditional=True, as_attachment=extensao not in tipos_inline)
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    resposta.cache_control.private = True
    resposta.cache_control.no_cache = True
    return resposta


@pagina_bp.route("/aulas/<int:id>/material")
def material_aula(id):
    aula = obter_conteudo(id)
    material = MaterialService.preparar(aula)
    if material["caminho"] is None:
        abort(404, description="Esta aula não possui um arquivo local disponível.")
    return enviar_material(material["caminho"])


def exigir_aluno():
    if g.usuario.tipo != "aluno":
        abort(403, description="Esta página é exclusiva do aluno.")


@pagina_bp.route("/")
def inicio():
    if g.usuario.tipo == "professor":
        return redirect(url_for("pagina.professor_cursos"))
    return redirect(url_for("pagina.aluno_cursos"))


@pagina_bp.route("/meu-perfil")
def perfil():
    return render_template("perfil.html", titulo="Meu perfil")


@pagina_bp.route("/aluno/cursos")
def aluno_cursos():
    exigir_aluno()
    cursos = []
    busca = request.args.get("busca", "")
    inscricoes = AcessoService.listar_inscricoes(g.usuario)
    for curso in AcessoService.listar_cursos(g.usuario):
        if busca.lower() in curso.nome.lower():
            cursos.append(curso)
    return render_template("aluno/cursos.html", titulo="Cursos da graduação", cursos=cursos,
                           inscricoes=inscricoes, busca=busca)


@pagina_bp.route("/aluno/minhas-inscricoes")
def aluno_inscricoes():
    exigir_aluno()
    return render_template("aluno/inscricoes.html", titulo="Meus cursos",
                           inscricoes=AcessoService.listar_inscricoes(g.usuario))


@pagina_bp.route("/aluno/cursos/<int:id>/aulas")
def aluno_aulas(id):
    exigir_aluno()
    curso = obter_curso(id, aulas=True)
    return render_template("aluno/aulas.html", titulo=curso.nome, curso=curso)


@pagina_bp.route("/professor/cursos")
@professor_obrigatorio
def professor_cursos():
    return render_template("professor/cursos.html", titulo="Meus cursos",
                           cursos=AcessoService.listar_cursos(g.usuario))


@pagina_bp.route("/professor/cursos/novo")
@professor_obrigatorio
def novo_curso():
    return render_template("professor/curso_form.html", titulo="Novo curso", curso=None,
                           trilhas=AcessoService.listar_trilhas(g.usuario))


@pagina_bp.route("/professor/cursos/<int:id>/editar")
@professor_obrigatorio
def editar_curso(id):
    return render_template("professor/curso_form.html", titulo="Editar curso",
                           curso=obter_curso(id, editar=True), trilhas=AcessoService.listar_trilhas(g.usuario))


@pagina_bp.route("/professor/cursos/<int:id>/aulas")
@professor_obrigatorio
def professor_aulas(id):
    curso = obter_curso(id, editar=True)
    return render_template("professor/aulas.html", titulo="Aulas do curso", curso=curso)


@pagina_bp.route("/professor/cursos/<int:id>/aulas/nova")
@professor_obrigatorio
def nova_aula(id):
    return render_template("professor/aula_form.html", titulo="Nova aula",
                           curso=obter_curso(id, editar=True), aula=None)


@pagina_bp.route("/professor/aulas/<int:id>/editar")
@professor_obrigatorio
def editar_aula(id):
    aula = obter_conteudo(id, editar=True)
    return render_template("professor/aula_form.html", titulo="Editar aula", curso=aula.curso, aula=aula)


@pagina_bp.route("/professor/trilhas")
@professor_obrigatorio
def professor_trilhas():
    return render_template("professor/trilhas.html", titulo="Trilhas",
                           trilhas=AcessoService.listar_trilhas(g.usuario), acesso=AcessoService)


@pagina_bp.route("/professor/trilhas/nova")
@professor_obrigatorio
def nova_trilha():
    return render_template("professor/trilha_form.html", titulo="Nova trilha", trilha=None)


@pagina_bp.route("/professor/trilhas/<int:id>/editar")
@professor_obrigatorio
def editar_trilha(id):
    return render_template("professor/trilha_form.html", titulo="Editar trilha",
                           trilha=obter_trilha(id, editar=True))


@pagina_bp.route("/professor/alunos")
@professor_obrigatorio
def professor_alunos():
    return render_template("professor/alunos.html", titulo="Alunos dos meus cursos",
                           inscricoes=AcessoService.listar_inscricoes(g.usuario))


@pagina_bp.route("/bucket/<path:arquivo>")
def arquivo_bucket(arquivo):
    for conteudo in ConteudoService.listar_todos():
        material = MaterialService.preparar(conteudo)
        if material["caminho"] == arquivo:
            if not AcessoService.pode_ver_aulas(g.usuario, conteudo.curso):
                abort(403, description="Você não tem acesso a este material.")
            return enviar_material(arquivo)
    abort(404, description="Material não encontrado.")


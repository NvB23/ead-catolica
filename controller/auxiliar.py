from flask import request, jsonify, flash, redirect, url_for, g
from werkzeug.exceptions import UnsupportedMediaType


def ler_dados():
    if request.is_json:
        dados = request.get_json()
        if type(dados) != dict:
            raise ValueError("Envie um objeto JSON.")
    elif request.mimetype in ("application/x-www-form-urlencoded", "multipart/form-data"):
        dados = request.form.to_dict()
        for campo in ("graduacao_id", "trilha_id", "curso_id", "aluno_id", "ordem", "progresso"):
            if campo in dados:
                try:
                    dados[campo] = int(dados[campo])
                except ValueError:
                    raise ValueError("Preencha corretamente o campo " + campo + ".")
        for campo in ("professor_ids", "graduacao_ids", "trilha_ids", "curso_ids"):
            dados[campo] = []
            for valor in request.form.getlist(campo):
                try:
                    dados[campo].append(int(valor))
                except ValueError:
                    raise ValueError("Selecione os vínculos corretamente.")
    else:
        raise UnsupportedMediaType("Envie JSON ou um formulário.")

    for campo in ("nome", "email", "senha", "sobre", "formacoes", "descricao", "capa", "texto", "url", "tipo"):
        if dados.get(campo) is not None and type(dados[campo]) != str:
            raise ValueError("O campo " + campo + " deve ser um texto.")
    for campo in ("graduacao_id", "trilha_id", "curso_id", "aluno_id", "ordem", "progresso"):
        if campo in dados and type(dados[campo]) != int:
            raise ValueError("O campo " + campo + " deve ser um número inteiro.")
    for campo in ("professor_ids", "graduacao_ids", "trilha_ids", "curso_ids"):
        if dados.get(campo) is not None:
            if type(dados[campo]) != list:
                raise ValueError("O campo " + campo + " deve ser uma lista de IDs.")
            for id in dados[campo]:
                if type(id) != int:
                    raise ValueError("Os IDs devem ser números inteiros.")
    return dados


def responder(mensagem, secao, status=200, curso_id=None):

    formulario = request.mimetype in ("application/x-www-form-urlencoded", "multipart/form-data")
    if not request.is_json and (formulario or request.path.endswith("/editar") or request.path.endswith("/remover")):
        categoria = "sucesso"
        if status >= 400:
            categoria = "erro"
        flash(mensagem, categoria)
        destino = "pagina.inicio"
        if secao == "trilha":
            destino = "pagina.professor_trilhas"
        elif secao == "inscricao":
            destino = "pagina.aluno_inscricoes"
        elif secao in ("aluno", "professor", "perfil"):
            destino = "pagina.perfil"
        elif secao == "conteudo":
            if curso_id is None:
                curso_id = request.form.get("curso_id", type=int)
            if curso_id is not None and g.usuario and g.usuario.tipo == "professor":
                return redirect(url_for("pagina.professor_aulas", id=curso_id), code=303)
        return redirect(url_for(destino), code=303)
    return jsonify({"mensagem": mensagem}), status

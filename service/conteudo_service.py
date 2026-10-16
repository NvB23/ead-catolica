from model.conteudo import Conteudo
from model.tipo_conteudo import TipoConteudo
from repository.conteudo_dao import ConteudoDAO
from repository.curso_dao import CursoDAO
from service.material_service import MaterialService


class ConteudoService:

    @staticmethod
    def validar_dados(nome, curso_id, tipo, ordem, texto, url):
        if nome is None or nome.strip() == "":
            raise ValueError("Informe o nome do conteúdo.")
        curso = CursoDAO.buscar_por_id(curso_id)
        if curso is None:
            raise ValueError("Curso não encontrado.")
        if type(ordem) != int or ordem < 0:
            raise ValueError("A ordem deve ser um número inteiro a partir de zero.")

        if tipo == "texto" or tipo == TipoConteudo.TEXTO:
            tipo = TipoConteudo.TEXTO
        elif tipo == "video" or tipo == TipoConteudo.VIDEO:
            tipo = TipoConteudo.VIDEO
        elif tipo == "audio" or tipo == TipoConteudo.AUDIO:
            tipo = TipoConteudo.AUDIO
        elif tipo == "imagem" or tipo == TipoConteudo.IMAGEM:
            tipo = TipoConteudo.IMAGEM
        else:
            raise ValueError("Tipo de conteúdo inválido.")

        if tipo == TipoConteudo.TEXTO:
            if texto is None or texto.strip() == "":
                raise ValueError("Informe o texto do conteúdo.")
        elif url is None or url.strip() == "":
            raise ValueError("Informe o caminho ou endereço do arquivo.")
        return curso, tipo

    @staticmethod
    def salvar(nome, descricao, curso_id, tipo, ordem=0, capa=None, texto=None, url=None):
        url = MaterialService.normalizar_url(url)
        curso, tipo = ConteudoService.validar_dados(nome, curso_id, tipo, ordem, texto, url)
        conteudo = Conteudo(nome=nome.strip(), descricao=descricao, curso=curso,
                            tipo=tipo, ordem=ordem, capa=capa, texto=texto, url=url)
        return ConteudoDAO.salvar(conteudo)

    @staticmethod
    def editar(id, nome, descricao, curso_id, tipo, ordem, capa, texto, url):
        url = MaterialService.normalizar_url(url)
        conteudo = ConteudoDAO.buscar_por_id(id)
        if conteudo is None:
            raise ValueError("Conteúdo não encontrado.")
        curso, tipo = ConteudoService.validar_dados(nome, curso_id, tipo, ordem, texto, url)
        return ConteudoDAO.editar(conteudo, nome.strip(), descricao, curso, tipo,
                                  ordem, capa, texto, url)

    @staticmethod
    def remover(id):
        conteudo = ConteudoDAO.buscar_por_id(id)
        if conteudo is None:
            raise ValueError("Conteúdo não encontrado.")
        return ConteudoDAO.remover(conteudo)

    @staticmethod
    def listar_todos():
        return ConteudoDAO.listar_todos()

    @staticmethod
    def buscar_por_id(id):
        return ConteudoDAO.buscar_por_id(id)

    @staticmethod
    def buscar_por_nome(nome):
        return ConteudoDAO.buscar_por_nome(nome)

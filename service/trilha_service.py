from model.trilha import Trilha
from repository.trilha_dao import TrilhaDAO
from repository.graduacao_dao import GraduacaoDAO


class TrilhaService:

    @staticmethod
    def validar_dados(nome, graduacao_ids):
        if nome is None or nome.strip() == "":
            raise ValueError("Informe o nome da trilha.")
        graduacoes = []
        if graduacao_ids is not None:
            for id in graduacao_ids:
                graduacao = GraduacaoDAO.buscar_por_id(id)
                if graduacao is None:
                    raise ValueError("Graduação não encontrada.")
                if graduacao not in graduacoes:
                    graduacoes.append(graduacao)
        return graduacoes

    @staticmethod
    def salvar(nome, graduacao_ids=None):
        graduacoes = TrilhaService.validar_dados(nome, graduacao_ids)
        trilha = Trilha(nome=nome.strip(), graduacoes=graduacoes)
        return TrilhaDAO.salvar(trilha)

    @staticmethod
    def editar(id, nome, graduacao_ids):
        trilha = TrilhaDAO.buscar_por_id(id)
        if trilha is None:
            raise ValueError("Trilha não encontrada.")
        graduacoes = TrilhaService.validar_dados(nome, graduacao_ids)
        return TrilhaDAO.editar(trilha, nome.strip(), graduacoes)

    @staticmethod
    def remover(id):
        trilha = TrilhaDAO.buscar_por_id(id)
        if trilha is None:
            raise ValueError("Trilha não encontrada.")
        for curso in trilha.cursos:
            if curso.inscricoes:
                raise ValueError("A trilha possui um curso com alunos inscritos.")
        return TrilhaDAO.remover(trilha)

    @staticmethod
    def listar_todos():
        return TrilhaDAO.listar_todos()

    @staticmethod
    def buscar_por_id(id):
        return TrilhaDAO.buscar_por_id(id)

    @staticmethod
    def buscar_por_nome(nome):
        return TrilhaDAO.buscar_por_nome(nome)

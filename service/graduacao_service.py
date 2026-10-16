from model.graduacao import Graduacao
from repository.graduacao_dao import GraduacaoDAO
from repository.professor_dao import ProfessorDAO
from repository.trilha_dao import TrilhaDAO


class GraduacaoService:

    @staticmethod
    def validar_dados(nome, professor_ids, trilha_ids, graduacao_id=None):
        if nome is None or nome.strip() == "":
            raise ValueError("Informe o nome da graduação.")
        for graduacao in GraduacaoDAO.listar_todos():
            if graduacao.nome.lower() == nome.strip().lower() and graduacao.id != graduacao_id:
                raise ValueError("Esta graduação já está cadastrada.")

        professores = []
        if professor_ids is not None:
            for id in professor_ids:
                professor = ProfessorDAO.buscar_por_id(id)
                if professor is None:
                    raise ValueError("Professor não encontrado.")
                if professor not in professores:
                    professores.append(professor)

        trilhas = []
        if trilha_ids is not None:
            for id in trilha_ids:
                trilha = TrilhaDAO.buscar_por_id(id)
                if trilha is None:
                    raise ValueError("Trilha não encontrada.")
                if trilha not in trilhas:
                    trilhas.append(trilha)
        return professores, trilhas

    @staticmethod
    def salvar(nome, professor_ids=None, trilha_ids=None):
        professores, trilhas = GraduacaoService.validar_dados(nome, professor_ids, trilha_ids)
        graduacao = Graduacao(nome=nome.strip(), professores=professores, trilhas=trilhas)
        return GraduacaoDAO.salvar(graduacao)

    @staticmethod
    def editar(id, nome, professor_ids, trilha_ids):
        graduacao = GraduacaoDAO.buscar_por_id(id)
        if graduacao is None:
            raise ValueError("Graduação não encontrada.")
        professores, trilhas = GraduacaoService.validar_dados(nome, professor_ids, trilha_ids, id)
        return GraduacaoDAO.editar(graduacao, nome.strip(), professores, trilhas)

    @staticmethod
    def remover(id):
        graduacao = GraduacaoDAO.buscar_por_id(id)
        if graduacao is None:
            raise ValueError("Graduação não encontrada.")
        if graduacao.alunos:
            raise ValueError("A graduação possui alunos cadastrados.")
        return GraduacaoDAO.remover(graduacao)

    @staticmethod
    def listar_todos():
        return GraduacaoDAO.listar_todos()

    @staticmethod
    def buscar_por_id(id):
        return GraduacaoDAO.buscar_por_id(id)

    @staticmethod
    def buscar_por_nome(nome):
        return GraduacaoDAO.buscar_por_nome(nome)

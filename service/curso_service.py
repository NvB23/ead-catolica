from model.curso import Curso
from repository.curso_dao import CursoDAO
from repository.trilha_dao import TrilhaDAO
from repository.professor_dao import ProfessorDAO


class CursoService:

    @staticmethod
    def validar_dados(nome, trilha_id, professor_ids):
        if nome is None or nome.strip() == "":
            raise ValueError("Informe o nome do curso.")
        trilha = TrilhaDAO.buscar_por_id(trilha_id)
        if trilha is None:
            raise ValueError("Trilha não encontrada.")

        professores = []
        if professor_ids is not None:
            for id in professor_ids:
                professor = ProfessorDAO.buscar_por_id(id)
                if professor is None:
                    raise ValueError("Professor não encontrado.")
                if professor not in professores:
                    professores.append(professor)
        return trilha, professores

    @staticmethod
    def salvar(nome, descricao, capa, trilha_id, professor_ids=None):
        trilha, professores = CursoService.validar_dados(nome, trilha_id, professor_ids)
        curso = Curso(nome=nome.strip(), descricao=descricao, capa=capa,
                      trilha=trilha, professores=professores)
        return CursoDAO.salvar(curso)

    @staticmethod
    def editar(id, nome, descricao, capa, trilha_id, professor_ids):
        curso = CursoDAO.buscar_por_id(id)
        if curso is None:
            raise ValueError("Curso não encontrado.")
        trilha, professores = CursoService.validar_dados(nome, trilha_id, professor_ids)
        return CursoDAO.editar(curso, nome.strip(), descricao, capa, trilha, professores)

    @staticmethod
    def remover(id):
        curso = CursoDAO.buscar_por_id(id)
        if curso is None:
            raise ValueError("Curso não encontrado.")
        if curso.inscricoes:
            raise ValueError("O curso possui alunos inscritos.")
        return CursoDAO.remover(curso)

    @staticmethod
    def listar_todos():
        return CursoDAO.listar_todos()

    @staticmethod
    def buscar_por_id(id):
        return CursoDAO.buscar_por_id(id)

    @staticmethod
    def buscar_por_nome(nome):
        return CursoDAO.buscar_por_nome(nome)

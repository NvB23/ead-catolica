from model.inscricao import Inscricao
from repository.inscricao_dao import InscricaoDAO
from repository.aluno_dao import AlunoDAO
from repository.curso_dao import CursoDAO


class InscricaoService:

    @staticmethod
    def salvar(aluno_id, curso_id):
        aluno = AlunoDAO.buscar_por_id(aluno_id)
        if aluno is None:
            raise ValueError("Aluno não encontrado.")
        curso = CursoDAO.buscar_por_id(curso_id)
        if curso is None:
            raise ValueError("Curso não encontrado.")
        if InscricaoDAO.buscar_por_aluno_e_curso(aluno_id, curso_id) is not None:
            raise ValueError("O aluno já está inscrito neste curso.")

        inscricao = Inscricao(aluno=aluno, curso=curso, progresso=0, concluido=False)
        return InscricaoDAO.salvar(inscricao)

    @staticmethod
    def editar(id, progresso):
        raise ValueError("A atualização de progresso está desativada.")

    @staticmethod
    def remover(id):
        inscricao = InscricaoDAO.buscar_por_id(id)
        if inscricao is None:
            raise ValueError("Inscrição não encontrada.")
        return InscricaoDAO.remover(inscricao)

    @staticmethod
    def listar_todos():
        return InscricaoDAO.listar_todos()

    @staticmethod
    def buscar_por_id(id):
        return InscricaoDAO.buscar_por_id(id)

    @staticmethod
    def buscar_por_aluno(aluno_id):
        return InscricaoDAO.buscar_por_aluno(aluno_id)

    @staticmethod
    def buscar_por_curso(curso_id):
        return InscricaoDAO.buscar_por_curso(curso_id)

    @staticmethod
    def buscar_por_aluno_e_curso(aluno_id, curso_id):
        return InscricaoDAO.buscar_por_aluno_e_curso(aluno_id, curso_id)

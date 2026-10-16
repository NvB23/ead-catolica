from model.professor import Professor
from repository.professor_dao import ProfessorDAO
from repository.aluno_dao import AlunoDAO
from repository.graduacao_dao import GraduacaoDAO
from repository.curso_dao import CursoDAO
from werkzeug.security import generate_password_hash


class ProfessorService:

    @staticmethod
    def validar_dados(nome, email, senha, graduacao_ids, curso_ids, professor_id=None):
        if nome is None or nome.strip() == "":
            raise ValueError("Informe o nome do professor.")
        if email is None or email.strip() == "" or "@" not in email:
            raise ValueError("Informe um e-mail válido.")
        if senha is None or senha.strip() == "":
            raise ValueError("Informe a senha.")

        for professor in ProfessorDAO.listar_todos():
            if professor.email.lower() == email.strip().lower() and professor.id != professor_id:
                raise ValueError("Este e-mail já está cadastrado.")
        for aluno in AlunoDAO.listar_todos():
            if aluno.email.lower() == email.strip().lower():
                raise ValueError("Este e-mail já está cadastrado.")

        graduacoes = []
        if graduacao_ids is not None:
            for id in graduacao_ids:
                graduacao = GraduacaoDAO.buscar_por_id(id)
                if graduacao is None:
                    raise ValueError("Graduação não encontrada.")
                if graduacao not in graduacoes:
                    graduacoes.append(graduacao)

        cursos = []
        if curso_ids is not None:
            for id in curso_ids:
                curso = CursoDAO.buscar_por_id(id)
                if curso is None:
                    raise ValueError("Curso não encontrado.")
                if curso not in cursos:
                    cursos.append(curso)
        return graduacoes, cursos

    @staticmethod
    def salvar(nome, email, senha, sobre=None, formacoes=None, graduacao_ids=None, curso_ids=None):
        graduacoes, cursos = ProfessorService.validar_dados(
            nome, email, senha, graduacao_ids, curso_ids)
        professor = Professor(nome=nome.strip(), email=email.strip().lower(), senha=generate_password_hash(senha),
                              sobre=sobre, formacoes=formacoes, graduacoes=graduacoes, cursos=cursos)
        return ProfessorDAO.salvar(professor)

    @staticmethod
    def editar(id, nome, email, senha, sobre, formacoes, graduacao_ids, curso_ids):
        professor = ProfessorDAO.buscar_por_id(id)
        if professor is None:
            raise ValueError("Professor não encontrado.")
        senha_salva = professor.senha
        if senha:
            if senha.strip() == "":
                raise ValueError("Informe uma senha válida.")
            senha_salva = generate_password_hash(senha)
        graduacoes, cursos = ProfessorService.validar_dados(
            nome, email, senha_salva, graduacao_ids, curso_ids, id)
        return ProfessorDAO.editar(professor, nome.strip(), email.strip().lower(), senha_salva,
                                   sobre, formacoes, graduacoes, cursos)

    @staticmethod
    def remover(id):
        professor = ProfessorDAO.buscar_por_id(id)
        if professor is None:
            raise ValueError("Professor não encontrado.")
        return ProfessorDAO.remover(professor)

    @staticmethod
    def listar_todos():
        return ProfessorDAO.listar_todos()

    @staticmethod
    def buscar_por_id(id):
        return ProfessorDAO.buscar_por_id(id)

    @staticmethod
    def buscar_por_nome(nome):
        return ProfessorDAO.buscar_por_nome(nome)

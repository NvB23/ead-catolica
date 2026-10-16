from model.aluno import Aluno
from repository.aluno_dao import AlunoDAO
from repository.professor_dao import ProfessorDAO
from repository.graduacao_dao import GraduacaoDAO
from werkzeug.security import generate_password_hash


class AlunoService:

    @staticmethod
    def validar_dados(nome, email, senha, graduacao_id, aluno_id=None):
        if nome is None or nome.strip() == "":
            raise ValueError("Informe o nome do aluno.")
        if email is None or email.strip() == "" or "@" not in email:
            raise ValueError("Informe um e-mail válido.")
        if senha is None or senha.strip() == "":
            raise ValueError("Informe a senha.")

        for aluno in AlunoDAO.listar_todos():
            if aluno.email.lower() == email.strip().lower() and aluno.id != aluno_id:
                raise ValueError("Este e-mail já está cadastrado.")
        for professor in ProfessorDAO.listar_todos():
            if professor.email.lower() == email.strip().lower():
                raise ValueError("Este e-mail já está cadastrado.")

        graduacao = GraduacaoDAO.buscar_por_id(graduacao_id)
        if graduacao is None:
            raise ValueError("Graduação não encontrada.")
        return graduacao

    @staticmethod
    def salvar(nome, email, senha, graduacao_id):
        graduacao = AlunoService.validar_dados(nome, email, senha, graduacao_id)
        aluno = Aluno(nome=nome.strip(), email=email.strip().lower(),
                      senha=generate_password_hash(senha), graduacao=graduacao)
        return AlunoDAO.salvar(aluno)

    @staticmethod
    def editar(id, nome, email, senha, graduacao_id):
        aluno = AlunoDAO.buscar_por_id(id)
        if aluno is None:
            raise ValueError("Aluno não encontrado.")
        senha_salva = aluno.senha
        if senha:
            if senha.strip() == "":
                raise ValueError("Informe uma senha válida.")
            senha_salva = generate_password_hash(senha)
        graduacao = AlunoService.validar_dados(nome, email, senha_salva, graduacao_id, id)
        return AlunoDAO.editar(aluno, nome.strip(), email.strip().lower(), senha_salva, graduacao)

    @staticmethod
    def remover(id):
        aluno = AlunoDAO.buscar_por_id(id)
        if aluno is None:
            raise ValueError("Aluno não encontrado.")
        return AlunoDAO.remover(aluno)

    @staticmethod
    def listar_todos():
        return AlunoDAO.listar_todos()

    @staticmethod
    def buscar_por_id(id):
        return AlunoDAO.buscar_por_id(id)

    @staticmethod
    def buscar_por_nome(nome):
        return AlunoDAO.buscar_por_nome(nome)

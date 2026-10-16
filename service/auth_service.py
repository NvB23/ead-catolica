from werkzeug.security import check_password_hash, generate_password_hash
from repository.pessoa_dao import PessoaDAO


class AuthService:

    @staticmethod
    def autenticar(email, senha):
        if not email or not senha:
            raise ValueError("Informe o e-mail e a senha.")
        pessoa = PessoaDAO.buscar_por_email(email.strip().lower())
        if pessoa is None or pessoa.tipo not in ("aluno", "professor"):
            return None
        if pessoa.senha.startswith("scrypt:") or pessoa.senha.startswith("pbkdf2:"):
            if check_password_hash(pessoa.senha, senha):
                return pessoa
            return None


        if pessoa.senha == senha:
            if not PessoaDAO.atualizar_senha(pessoa, generate_password_hash(senha)):
                raise ValueError("Não foi possível atualizar a senha. Tente novamente.")
            return pessoa
        return None

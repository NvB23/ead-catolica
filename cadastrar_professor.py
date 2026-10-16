from getpass import getpass
from servidor import app
from db.dados_iniciais import listar_graduacoes_fixas
from service.professor_service import ProfessorService


def cadastrar_professor():
    with app.app_context():
        print("Cadastro de professor")
        nome = input("Nome: ").strip()
        email = input("E-mail: ").strip()
        senha = getpass("Senha: ")
        if senha != getpass("Confirme a senha: "):
            print("As senhas não conferem.")
            return
        graduacoes = listar_graduacoes_fixas()
        print("Graduações disponíveis:")
        for graduacao in graduacoes:
            print(str(graduacao.id) + " - " + graduacao.nome)
        escolha = input("IDs das graduações, separados por vírgula: ")
        ids = []
        try:
            for valor in escolha.split(","):
                id = int(valor.strip())
                permitida = False
                for graduacao in graduacoes:
                    if graduacao.id == id:
                        permitida = True
                if not permitida:
                    raise ValueError("Graduação não encontrada.")
                if id not in ids:
                    ids.append(id)
            if not ids:
                raise ValueError("Selecione pelo menos uma graduação.")
            if ProfessorService.salvar(nome, email, senha, graduacao_ids=ids):
                print("Professor cadastrado. Use o e-mail e a senha na página de login.")
            else:
                print("Não foi possível cadastrar o professor.")
        except ValueError as erro:
            print(str(erro))


if __name__ == "__main__":
    cadastrar_professor()

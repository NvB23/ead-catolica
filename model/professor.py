from pessoa import Pessoa

class Professor(Pessoa):

    def __init__(self, id, nome, email, senha, sobre) -> None:
        super().__init__(id, nome, email, senha)

        self.formacoes = []
        self.sobre = sobre
        self.graduacoes = []
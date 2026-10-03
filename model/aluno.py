from pessoa import Pessoa

class Aluno(Pessoa):

    def __init__(self, id, nome, email, senha, curso_academico) -> None:
        super().__init__(id, nome, email, senha)
        self.certificados = []
        self.graduacao = curso_academico
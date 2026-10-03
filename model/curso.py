class Curso():

    def __init__(self, id, nome, descricao) -> None:
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.conteudos = []
        self.professores = []
        self.capa = None
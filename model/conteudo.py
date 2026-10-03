class Conteudo():

    def __init__(self, id, nome, descricao, curso, tipo) -> None:
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.curso = curso
        self.capa = None
        self.tipo = tipo
        self.ordem = 0
        self.texto = None
        self.url = None

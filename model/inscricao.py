from datetime import datetime

class Inscricao():

    def __init__(self, id, aluno, curso) -> None:
        self.id = id
        self.aluno = aluno
        self.curso = curso
        self.progresso = 0
        self.concluido = False
        self.data_inicio = datetime.now
        self.data_conclusao = None
        
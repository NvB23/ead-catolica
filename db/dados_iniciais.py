from repository.graduacao_dao import GraduacaoDAO
from model.graduacao import Graduacao

NOMES_GRADUACOES = [
    "Ciência da Computação", "Marketing", "Filosofia", "Educação Física", "Direito"
]


def cadastrar_graduacoes():
    existentes = GraduacaoDAO.listar_todos()
    for nome in NOMES_GRADUACOES:
        encontrada = False
        for graduacao in existentes:
            if graduacao.nome.strip().lower() == nome.lower():
                encontrada = True
                break
        if not encontrada:
            if not GraduacaoDAO.salvar(Graduacao(nome=nome)):
                raise RuntimeError("Não foi possível cadastrar a graduação " + nome + ".")


def listar_graduacoes_fixas():
    lista = []
    for nome in NOMES_GRADUACOES:
        for graduacao in GraduacaoDAO.listar_todos():
            if graduacao.nome.strip().lower() == nome.lower():
                lista.append(graduacao)
                break
    return lista

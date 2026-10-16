from repository.curso_dao import CursoDAO
from repository.trilha_dao import TrilhaDAO
from repository.inscricao_dao import InscricaoDAO


class AcessoService:

    @staticmethod
    def pode_ver_curso(usuario, curso):
        if usuario.tipo == "professor":
            return AcessoService.pode_editar_curso(usuario, curso)
        for graduacao in curso.trilha.graduacoes:
            if graduacao.id == usuario.graduacao_id:
                return True
        return False

    @staticmethod
    def pode_editar_curso(usuario, curso):
        if usuario.tipo != "professor":
            return False
        for professor in curso.professores:
            if professor.id == usuario.id:
                return True
        return False

    @staticmethod
    def pode_ver_aulas(usuario, curso):
        if not AcessoService.pode_ver_curso(usuario, curso):
            return False
        if usuario.tipo == "professor":
            return True
        return InscricaoDAO.buscar_por_aluno_e_curso(usuario.id, curso.id) is not None

    @staticmethod
    def pode_usar_trilha(usuario, trilha):
        if usuario.tipo != "professor" or not trilha.graduacoes:
            return False
        for graduacao in trilha.graduacoes:
            if graduacao not in usuario.graduacoes:
                return False
        return True

    @staticmethod
    def pode_gerenciar_trilha(usuario, trilha):
        if not AcessoService.pode_usar_trilha(usuario, trilha):
            return False
        for curso in trilha.cursos:
            if not AcessoService.pode_editar_curso(usuario, curso):
                return False
        return True

    @staticmethod
    def listar_cursos(usuario):
        lista = []
        for curso in CursoDAO.listar_todos():
            if AcessoService.pode_ver_curso(usuario, curso):
                lista.append(curso)
        return lista

    @staticmethod
    def listar_trilhas(usuario):
        lista = []
        for trilha in TrilhaDAO.listar_todos():
            if usuario.tipo == "professor":
                if AcessoService.pode_usar_trilha(usuario, trilha):
                    lista.append(trilha)
            else:
                for graduacao in trilha.graduacoes:
                    if graduacao.id == usuario.graduacao_id:
                        lista.append(trilha)
                        break
        return lista

    @staticmethod
    def pode_ver_inscricao(usuario, inscricao):
        if usuario.tipo == "aluno" and inscricao.aluno_id != usuario.id:
            return False
        return AcessoService.pode_ver_curso(usuario, inscricao.curso)

    @staticmethod
    def listar_inscricoes(usuario):
        lista = []
        for inscricao in InscricaoDAO.listar_todos():
            if AcessoService.pode_ver_inscricao(usuario, inscricao):
                lista.append(inscricao)
        return lista

    @staticmethod
    def validar_graduacoes_professor(usuario, ids):
        if not ids:
            raise ValueError("Selecione pelo menos uma graduação.")
        for id in ids:
            encontrada = False
            for graduacao in usuario.graduacoes:
                if graduacao.id == id:
                    encontrada = True
                    break
            if not encontrada:
                raise ValueError("Selecione apenas as suas graduações.")

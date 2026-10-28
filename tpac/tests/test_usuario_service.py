import unittest

from services.usuario_service import UsuarioService


class UsuarioFake:
    def __init__(self, id, nome, email, estilo_instrucao):
        self.id = id
        self.nome = nome
        self.email = email
        self.estilo_instrucao = estilo_instrucao


class UsuarioRepositoryFake:
    """
    Substitui o UsuarioRepository real.
    Guarda tudo em um dicionário na memória, sem MySQL.
    """
    def __init__(self):
        self.usuarios_por_nome = {}
        self.usuarios_por_email = {}
        self._proximo_id = 1

    def buscar_por_nome(self, nome):
        return self.usuarios_por_nome.get(nome)

    def buscar_por_email(self, email):
        return self.usuarios_por_email.get(email)

    def criar(self, nome, email, senha, estilo_instrucao):
        usuario = UsuarioFake(self._proximo_id, nome, email, estilo_instrucao)
        self.usuarios_por_nome[nome] = usuario
        self.usuarios_por_email[email] = usuario
        self._proximo_id += 1
        return usuario


class TestUsuarioServiceNomeMinimo(unittest.TestCase):
    def setUp(self):
        self.service = UsuarioService()
        self.service.repository = UsuarioRepositoryFake()

    def test_cria_usuario_valido(self):
        usuario = self.service.cadastrar_usuario("Ana", "ana@teste.com", "senha123")
        self.assertEqual(usuario.nome, "Ana")

    def test_rejeita_nome_com_menos_de_3_caracteres(self):
        with self.assertRaisesRegex(ValueError, "pelo menos 3 caracteres"):
            self.service.cadastrar_usuario("Al", "al@teste.com", "senha123")


if __name__ == "__main__":
    unittest.main()
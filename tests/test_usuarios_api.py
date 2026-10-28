import unittest

from fastapi.testclient import TestClient

from api_app import app


class TestUsuariosAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_usuarios_retorna_200_com_dados(self):
        resposta = self.client.get("/usuarios")
        self.assertEqual(resposta.status_code, 200)
        corpo = resposta.json()
        self.assertIn("dados", corpo)
        self.assertIsInstance(corpo["dados"], list)

    def test_post_usuarios_com_nome_duplicado_retorna_422(self):
        resposta = self.client.post("/usuarios", json={
            "nome": "gustavo",
            "email": "email_qualquer@teste.com",
            "senha": "senha123",
            "estilo_instrucao": "direto"
        })
        self.assertEqual(resposta.status_code, 422)
        corpo = resposta.json()
        self.assertIn("Nome já existente", corpo["detail"])


if __name__ == "__main__":
    unittest.main()
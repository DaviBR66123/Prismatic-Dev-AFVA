import re

from repositories.usuario_repository import UsuarioRepository
from ui.utils import gerar_hash_senha

ESTILOS_VALIDOS = ("direto", "detalhado", "tdah", "tea", "depressao")
PADRAO_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class UsuarioService:
    """
    Decide e valida as regras de cadastro de usuário.
    Quem acessa o banco é sempre o UsuarioRepository.
    """

    def __init__(self):
        self.repository = UsuarioRepository()

    def cadastrar_usuario(self, nome: str, email: str, senha: str, estilo_instrucao: str = "direto"):
        nome = (nome or "").strip()
        email = (email or "").strip().lower()
        senha = (senha or "").strip()

        if not nome or not nome.replace(" ", "").isalpha():
            raise ValueError("Nome inválido.")

        if len(nome) < 3:
            raise ValueError("O nome precisa ter pelo menos 3 caracteres.")

        if self.repository.buscar_por_nome(nome):
            raise ValueError("Nome já existente.")
        if not email or not re.match(PADRAO_EMAIL, email):
            raise ValueError("Email inválido.")

        if self.repository.buscar_por_email(email):
            raise ValueError("Email já cadastrado.")

        if not senha or len(senha) < 6:
            raise ValueError("Senha inválida (mínimo 6 caracteres).")

        if estilo_instrucao not in ESTILOS_VALIDOS:
            estilo_instrucao = "direto"

        senha_hash = gerar_hash_senha(senha)

        return self.repository.criar(
            nome=nome,
            email=email,
            senha=senha_hash,
            estilo_instrucao=estilo_instrucao
        )
    def atualizar_usuario(self, usuario_id: int, email: str, estilo_instrucao: str):
        email = (email or "").strip().lower()

        usuario_atual = self.repository.buscar_por_id(usuario_id)
        if usuario_atual is None:
            raise ValueError("Usuário não encontrado.")

        if not email or not re.match(PADRAO_EMAIL, email):
            raise ValueError("Email inválido.")

        usuario_com_esse_email = self.repository.buscar_por_email(email)
        if usuario_com_esse_email and usuario_com_esse_email.id != usuario_id:
            raise ValueError("Email já cadastrado.")

        if estilo_instrucao not in ESTILOS_VALIDOS:
            estilo_instrucao = usuario_atual.estilo_instrucao

        return self.repository.atualizar(usuario_id, email, estilo_instrucao)
    def autenticar(self, email: str, senha: str):
        email = (email or "").strip().lower()
        senha = (senha or "").strip()

        usuario = self.repository.buscar_por_email(email)

        if usuario is None or usuario.senha != gerar_hash_senha(senha):
            raise ValueError("Email ou senha incorretos.")

        return usuario
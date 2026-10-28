from ui.utils import exibir_cabecalho
from services.usuario_service import UsuarioService
from auth_token import criar_token

OPCOES_ESTILO = {
    "1": "direto",
    "2": "detalhado",
    "3": "tdah",
    "4": "tea",
    "5": "depressao",
}


def criar_usuario_menu(dados: dict):
    """
    Mesma tela e mesmas perguntas de antes.
    A diferença é que quem decide se pode cadastrar agora é o UsuarioService,
    e quem salva é o UsuarioRepository (por trás do Service).
    """
    exibir_cabecalho("CRIAR NOVO PERFIL")
    nome = input("Digite o nome do usuário: ").strip()
    email = input("Digite seu email: ").strip().lower()
    senha = input("Crie uma senha: ").strip()

    print("\n--- Preferências de Comunicação ---")
    print("1. Direto (passo a passo curto e direto)")
    print("2. Detalhado (explicativo, passo a passo)")
    print("3. TDAH (frases curtas, uma ação por linha)")
    print("4. TEA (literal, específico, sem ambiguidade)")
    print("5. Depressão (calmo, sem cobrança, acolhedor)")
    pref = input("Opção: ").strip()
    estilo = OPCOES_ESTILO.get(pref, "direto")

    service = UsuarioService()
    
    try:
        usuario = service.cadastrar_usuario(nome, email, senha, estilo)
    except ValueError as erro:
        input(f"\n{erro} Pressione Enter.")
        return
    except Exception:
        input("\nNão foi possível concluir o cadastro. Tente novamente mais tarde. Pressione Enter.")
        return
    # mantém o dicionário em memória sincronizado para o resto da sessão
    dados[usuario.nome] = {
        "email": usuario.email,
        "senha": usuario.senha,
        "preferencias": {"estilo_instrucao": usuario.estilo_instrucao},
        "tarefas_diarias": [],
        "tarefas_educacionais": []
    }

    input(f"\nPerfil [{usuario.nome}] criado! Pressione Enter.")


def listar_usuarios_api(busca: str = None, limite: int = None):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    service = UsuarioService()
    usuarios = service.repository.listar_todos(busca=busca, limite=limite)
    return [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "estilo_instrucao": u.estilo_instrucao
        }
        for u in usuarios
    ]


def criar_usuario_api(nome, email, senha, estilo_instrucao="direto"):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    Deixa o ValueError "subir" para quem chamou decidir o que fazer.
    """
    service = UsuarioService()
    usuario = service.cadastrar_usuario(nome, email, senha, estilo_instrucao)
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "estilo_instrucao": usuario.estilo_instrucao
    }


def buscar_usuario_api(usuario_id: int):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    service = UsuarioService()
    usuario = service.repository.buscar_por_id(usuario_id)

    if usuario is None:
        raise ValueError("Usuário não encontrado.")

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "estilo_instrucao": usuario.estilo_instrucao
    }
def atualizar_usuario_api(usuario_id: int, email: str, estilo_instrucao: str):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    service = UsuarioService()
    usuario = service.atualizar_usuario(usuario_id, email, estilo_instrucao)
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "estilo_instrucao": usuario.estilo_instrucao
    }
def excluir_usuario_api(usuario_id: int):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    service = UsuarioService()
    usuario = service.repository.buscar_por_id(usuario_id)

    if usuario is None:
        raise ValueError("Usuário não encontrado.")

    service.repository.excluir(usuario_id)
def login_api(email: str, senha: str):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    service = UsuarioService()
    usuario = service.autenticar(email, senha)
    token = criar_token(usuario.id, usuario.nome, usuario.papel)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "papel": usuario.papel
        }
    }
    
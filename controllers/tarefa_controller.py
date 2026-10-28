from repositories.tarefa_repository import TarefaRepository

TIPOS_VALIDOS = ("tarefas_diarias", "tarefas_educacionais")


def listar_tarefas_api(usuario_id: int):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    repository = TarefaRepository()
    tarefas = repository.listar_por_usuario(usuario_id)
    return [
        {
            "id": t.id,
            "usuario_id": t.usuario_id,
            "tipo": t.tipo,
            "titulo": t.titulo,
            "concluida": t.concluida
        }
        for t in tarefas
    ]


def criar_tarefa_api(usuario_id: int, tipo: str, titulo: str):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    titulo = (titulo or "").strip()

    if tipo not in TIPOS_VALIDOS:
        raise ValueError("Tipo inválido.")

    if not titulo:
        raise ValueError("Título não pode ficar vazio.")

    repository = TarefaRepository()
    tarefa = repository.criar(usuario_id, tipo, titulo)
    return {
        "id": tarefa.id,
        "usuario_id": tarefa.usuario_id,
        "tipo": tarefa.tipo,
        "titulo": tarefa.titulo,
        "concluida": tarefa.concluida
    }


def alternar_status_api(usuario_id: int, tarefa_id: int):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    repository = TarefaRepository()
    tarefa = repository.buscar_por_id(tarefa_id)

    if tarefa is None or tarefa.usuario_id != usuario_id:
        raise ValueError("Tarefa não encontrada.")

    tarefa_atualizada = repository.alternar_status(tarefa_id)
    return {
        "id": tarefa_atualizada.id,
        "usuario_id": tarefa_atualizada.usuario_id,
        "tipo": tarefa_atualizada.tipo,
        "titulo": tarefa_atualizada.titulo,
        "concluida": tarefa_atualizada.concluida
    }
def excluir_tarefa_api(usuario_id: int, tarefa_id: int):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    repository = TarefaRepository()
    tarefa = repository.buscar_por_id(tarefa_id)

    if tarefa is None or tarefa.usuario_id != usuario_id:
        raise ValueError("Tarefa não encontrada.")

    repository.excluir(tarefa_id)
from repositories.passo_repository import PassoRepository


def listar_passos_api(tarefa_id: int):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    repository = PassoRepository()
    passos = repository.listar_por_tarefa(tarefa_id)
    return [
        {
            "id": p.id,
            "tarefa_id": p.tarefa_id,
            "texto": p.texto,
            "concluido": p.concluido,
            "ordem": p.ordem
        }
        for p in passos
    ]
def alternar_status_api(tarefa_id: int, passo_id: int):
    """
    Versão sem input()/print(), pensada para ser chamada pela API.
    """
    repository = PassoRepository()
    passo = repository.buscar_por_id(passo_id)

    if passo is None or passo.tarefa_id != tarefa_id:
        raise ValueError("Passo não encontrado.")

    passo_atualizado = repository.alternar_status(passo_id)
    return {
        "id": passo_atualizado.id,
        "tarefa_id": passo_atualizado.tarefa_id,
        "texto": passo_atualizado.texto,
        "concluido": passo_atualizado.concluido,
        "ordem": passo_atualizado.ordem
    }
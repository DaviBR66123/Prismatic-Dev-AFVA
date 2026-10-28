from fastapi import APIRouter, HTTPException

from controllers.passo_controller import listar_passos_api, alternar_status_api

router = APIRouter(
    tags=["passos"]
)


@router.get("/tarefas/{tarefa_id}/passos")
def listar_passos_da_tarefa(tarefa_id: int):
    return {
        "dados": listar_passos_api(tarefa_id)
    }


@router.patch("/tarefas/{tarefa_id}/passos/{passo_id}")
def alternar_status_passo(tarefa_id: int, passo_id: int):
    try:
        passo = alternar_status_api(tarefa_id, passo_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))

    return {"dados": passo}
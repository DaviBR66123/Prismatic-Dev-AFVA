from fastapi import FastAPI
from fastapi.security import HTTPBearer
from api.rotas_usuarios import router as usuarios_router
from api.rotas_tarefas import router as tarefas_router
from api.rotas_passos import router as passos_router
from api.rotas_auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TPaC API",
    description="API criada na Aula 04",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

app.include_router(usuarios_router)
app.include_router(tarefas_router)
app.include_router(passos_router)
app.include_router(auth_router)

@app.get("/")
def inicio():
    return {
        "sistema": "TPaC",
        "api": "funcionando"
    }
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.tarefa import Tarefa

load_dotenv()

DB_URL = (
    f"mysql+mysqlconnector://{os.getenv('DB_USER', 'root')}:"
    f"{os.getenv('DB_PASSWORD', '')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '3306')}/"
    f"{os.getenv('DB_NAME', 'tpac_db')}"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


class TarefaRepository:
    """
    Centraliza o acesso ao banco para a tabela tarefas.
    """

    def listar_por_usuario(self, usuario_id: int):
        session = SessionLocal()
        try:
            return session.query(Tarefa).filter(Tarefa.usuario_id == usuario_id).all()
        finally:
            session.close()

    def criar(self, usuario_id: int, tipo: str, titulo: str):
        session = SessionLocal()
        try:
            tarefa = Tarefa(
                usuario_id=usuario_id,
                tipo=tipo,
                titulo=titulo,
                concluida=False
            )
            session.add(tarefa)
            session.commit()
            session.refresh(tarefa)
            return tarefa
        finally:
            session.close()

    def buscar_por_id(self, tarefa_id: int):
        session = SessionLocal()
        try:
            return session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        finally:
            session.close()

    def alternar_status(self, tarefa_id: int):
        session = SessionLocal()
        try:
            tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
            tarefa.concluida = not tarefa.concluida
            session.commit()
            session.refresh(tarefa)
            return tarefa
        finally:
            session.close()

    def excluir(self, tarefa_id: int):
        session = SessionLocal()
        try:
            tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
            session.delete(tarefa)
            session.commit()
        finally:
            session.close()
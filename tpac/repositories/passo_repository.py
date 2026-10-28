import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.passo import Passo

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


class PassoRepository:
    """
    Centraliza o acesso ao banco para a tabela passos.
    """

    def listar_por_tarefa(self, tarefa_id: int):
        session = SessionLocal()
        try:
            return session.query(Passo).filter(Passo.tarefa_id == tarefa_id).order_by(Passo.ordem).all()
        finally:
            session.close()

    def buscar_por_id(self, passo_id: int):
        session = SessionLocal()
        try:
            return session.query(Passo).filter(Passo.id == passo_id).first()
        finally:
            session.close()

    def alternar_status(self, passo_id: int):
        session = SessionLocal()
        try:
            passo = session.query(Passo).filter(Passo.id == passo_id).first()
            passo.concluido = not passo.concluido
            session.commit()
            session.refresh(passo)
            return passo
        finally:
            session.close()
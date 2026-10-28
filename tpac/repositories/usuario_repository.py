import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.usuario import Usuario

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


class UsuarioRepository:
    """
    Centraliza todo o acesso ao banco para a tabela usuarios.
    Não valida nada, não decide nada, só busca e salva.
    """

    def listar_todos(self, busca: str = None, limite: int = None):
        session = SessionLocal()
        try:
            query = session.query(Usuario)

            if busca:
                query = query.filter(Usuario.nome.ilike(f"%{busca}%"))

            query = query.order_by(Usuario.nome)

            if limite:
                query = query.limit(limite)

            return query.all()
        finally:
            session.close()

    def buscar_por_nome(self, nome: str):
        session = SessionLocal()
        try:
            return session.query(Usuario).filter(Usuario.nome == nome).first()
        finally:
            session.close()

    def buscar_por_email(self, email: str):
        session = SessionLocal()
        try:
            return session.query(Usuario).filter(Usuario.email == email).first()
        finally:
            session.close()

    def buscar_por_id(self, usuario_id: int):
        session = SessionLocal()
        try:
            return session.query(Usuario).filter(Usuario.id == usuario_id).first()
        finally:
            session.close()

    def atualizar(self, usuario_id: int, email: str, estilo_instrucao: str):
        session = SessionLocal()
        try:
            usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
            usuario.email = email
            usuario.estilo_instrucao = estilo_instrucao
            session.commit()
            session.refresh(usuario)
            return usuario
        finally:
            session.close()
            
    def excluir(self, usuario_id: int):
        session = SessionLocal()
        try:
            usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
            session.delete(usuario)
            session.commit()
        finally:
            session.close()

    def criar(self, nome: str, email: str, senha: str, estilo_instrucao: str = "direto"):
        session = SessionLocal()
        try:
            usuario = Usuario(
                nome=nome,
                email=email,
                senha=senha,
                estilo_instrucao=estilo_instrucao
            )
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario
        finally:
            session.close()
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    estilo_instrucao = Column(
        Enum("direto", "detalhado", "tdah", "tea", "depressao"),
        nullable=False,
        default="direto"
    )
    papel = Column(
        Enum("usuario", "admin"),
        nullable=False,
        default="usuario"
    )
    criado_em = Column(TIMESTAMP, nullable=True)
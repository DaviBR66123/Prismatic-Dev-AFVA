from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP
from models.usuario import Base


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, nullable=False)
    tipo = Column(
        Enum("tarefas_diarias", "tarefas_educacionais"),
        nullable=False
    )
    titulo = Column(String(200), nullable=False)
    concluida = Column(Boolean, nullable=False, default=False)
    criado_em = Column(TIMESTAMP, nullable=True)
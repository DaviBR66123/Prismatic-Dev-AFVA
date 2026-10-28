from sqlalchemy import Column, Integer, String, Boolean, Text
from models.usuario import Base


class Passo(Base):
    __tablename__ = "passos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tarefa_id = Column(Integer, nullable=False)
    texto = Column(Text, nullable=False)
    concluido = Column(Boolean, nullable=False, default=False)
    ordem = Column(Integer, nullable=False, default=1)
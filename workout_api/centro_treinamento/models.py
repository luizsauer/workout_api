#workout_api\centro_treinamento\models.py
from sqlalchemy import Integer, String
from workout_api.atletas.models import AtletaModel
from workout_api.contrib.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship



class CentroTreinamentoModel(BaseModel):
    __tablename__ = 'centro_treinamento'
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    endereco: Mapped[str] = mapped_column(String(100), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(50), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    atleta: Mapped[list['AtletaModel']] = relationship(back_populates='centro_treinamento')
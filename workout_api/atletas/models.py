#workout_api\atletas\models.py
from datetime import datetime
from sqlalchemy import Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from workout_api.contrib.models import BaseModel

class AtletaModel(BaseModel):
    __tablename__ = 'atletas'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    data_nascimento: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    categoria: Mapped['CategoriaModel'] = relationship(back_populates='atleta', lazy='selectin')
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.pk_id', ondelete="CASCADE"))
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates='atleta', lazy='selectin')
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey('centro_treinamento.pk_id'))
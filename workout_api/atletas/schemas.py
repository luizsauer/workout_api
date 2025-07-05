#workout_api\atletas\schemas.py
from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.atletas.models import AtletaModel
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="Ronaldo", min_length=3, max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678901", min_length=11, max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=30)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=80.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.80)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", min_length=1, max_length=1)]
    data_nascimento: Annotated[str, Field(description="Data de nascimento do atleta", example="1990-01-01", min_length=10, max_length=10)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]

class AtletaIn(Atleta):
    pass
class AtletaOut(Atleta, OutMixin):
    # categoria: Annotated[str, Field(description="Categoria do atleta", example="Atletismo")]
    # centro_treinamento: Annotated[str, Field(description="Centro de treinamento do atleta", example="Centro de Treinamento")]
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, min_length=3, max_length=50, description="Nome do atleta", example="Ronaldo")]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", example=30)]

class AtletaSimplificadoOut(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta")]
    centro_treinamento: Annotated[str, Field(description="Nome do centro de treinamento")]
    categoria: Annotated[str, Field(description="Nome da categoria")]

    @classmethod
    def from_model(cls, atleta: 'AtletaModel'):
        return cls(
            nome=atleta.nome,
            centro_treinamento=atleta.centro_treinamento.nome if atleta.centro_treinamento else None,
            categoria=atleta.categoria.nome if atleta.categoria else None
        )
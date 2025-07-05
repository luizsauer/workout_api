#workout_api\centro_treinamento\schemas.py
from typing import Annotated, Optional

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="Centro de Treinamento", min_length=3, max_length=50)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", example="Av. Paulista, 1000", min_length=3, max_length=100)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de treinamento", example="João da Silva", min_length=3, max_length=50)]
    telefone: Annotated[str, Field(description="Telefone do centro de treinamento", example="1234567890", min_length=3, max_length=50)]
    
class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="Centro de Treinamento", min_length=3, max_length=50)]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="ID do centro de treinamento", example="123e4567-e89b-12d3-a456-426655440000")]
    
class CentroTreinamentoUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None,description="Nome do centro de treinamento", example="Centro de Treinamento", min_length=3, max_length=50)]
    endereco: Annotated[Optional[str], Field(None,description="Endereço do centro de treinamento", example="Av. Paulista, 1000", min_length=3, max_length=100)]
    proprietario: Annotated[Optional[str], Field(None,description="Proprietário do centro de treinamento", example="João da Silva", min_length=3, max_length=50)]
    telefone: Annotated[Optional[str], Field(None,description="Telefone do centro de treinamento", example="1234567890", min_length=3, max_length=50)]

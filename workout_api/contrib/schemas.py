#workout_api\contrib\schemas.py
from datetime import datetime
from typing import Annotated
from pydantic import UUID4, BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid" # nao aceita campos extras
        from_attributes = True # pode ser usado para criar um schema a partir de um model
        
class OutMixin(BaseSchema):
    id: Annotated[UUID4, Field(description="ID do atleta", example="123e4567-e89b-12d3-a456-426655440000")]
    created_at: Annotated[datetime, Field(description="Data de criação do atleta", example="2023-06-01T12:34:56Z")]
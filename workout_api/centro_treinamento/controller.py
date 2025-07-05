#workout_api\centro_treinamento\controller.py
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut, CentroTreinamentoUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate


router = APIRouter()

@router.post(
    "/",
    summary="Cria um novo Centro de Treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
)
async def post(
    db_session: DatabaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:

    try:
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
        
        db_session.add(centro_treinamento_model)
        await db_session.commit()
        
        return centro_treinamento_out
    
    except IntegrityError as e:
        await db_session.rollback()
        if "nome" in str(e).lower() or "centro_treinamento_nome_key" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f"Já existe um centro de treinamento cadastrado com o nome: {centro_treinamento_in.nome}"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro de integridade ao inserir o centro de treinamento: {str(e)}"
        )
        
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir o centro de treinamento: {str(e)}"
        )



@router.get(
    "/",
    summary="Consultar todos os Centros de Treinamento",
    status_code=status.HTTP_200_OK,
    response_model=Page[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency):
    query = select(CentroTreinamentoModel)
    return await sqlalchemy_paginate(db_session, query)



@router.get(
    "/{id}",
    summary="Consultar um Centro de Treinamento pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento_id: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Centro treinamento não encontrada no id: {id}")

    return centro_treinamento_id




@router.patch(
    "/{id}",
    summary="Editar um centro treinamento pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(id: UUID4, db_session: DatabaseDependency, ct_up: CentroTreinamentoUpdate = Body(...)) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Centro treinamento com id: {id} não encontrado")

    ct_update = ct_up.model_dump(exclude_unset=True)
    for key, value in ct_update.items():
        setattr(centro_treinamento, key, value)
        
    await db_session.commit()
    await db_session.refresh(centro_treinamento)

    return centro_treinamento


@router.delete(
    "/{id}",
    summary="Deletar um centro treinamento pelo ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def query(id: UUID4, db_session: DatabaseDependency) -> None:
    centro_treinamento: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Centro treinamento com id: {id} não encontrado")

    # Verifica se há atletas associados a este centro de treinamento
    from workout_api.atletas.models import AtletaModel
    atletas_associados = (
        await db_session.execute(select(AtletaModel).filter_by(centro_treinamento_id=centro_treinamento.pk_id))
    ).scalars().first()

    if atletas_associados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar o centro de treinamento pois existem atletas associados a ele"
        )

    await db_session.delete(centro_treinamento)
    await db_session.commit()

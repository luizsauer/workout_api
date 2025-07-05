#workout_api\atletas\controller.py
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from workout_api.atletas.models import AtletaModel
from workout_api.atletas.schemas import AtletaOut, AtletaIn, AtletaSimplificadoOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

router = APIRouter()

@router.post(
    "/",
    summary="Cria um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
):

    #categoria
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"A Categoria {categoria_nome} não foi encontrada")
    
    #centro de treinamento
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"A Centro de Treinamento {centro_treinamento_nome} não foi encontrada")
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()
        
    except IntegrityError as e:
        await db_session.rollback()
        if "cpf" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir o atleta: {str(e)}"
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir o atleta: {str(e)}"
        )

    return atleta_out


@router.get(
    "/",
    summary="Consultar todos os Atletas",
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaOut],
)
async def query(
    db_session: DatabaseDependency,
    nome: str = Query(None, description="Filtrar por nome do atleta"),
    cpf: str = Query(None, description="Filtrar por CPF do atleta")
):
    
    query_stmt = select(AtletaModel)

    if nome:
        query_stmt = query_stmt.filter(AtletaModel.nome.ilike(f"%{nome}%"))

    if cpf:
        query_stmt = query_stmt.filter(AtletaModel.cpf == cpf)

    atletas = (await db_session.execute(query_stmt)).scalars().all()
    return paginate([AtletaOut.model_validate(atleta) for atleta in atletas])


@router.get(
    "/{id}",
    summary="Consultar um atleta pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Atleta com id: {id} não encontrado")

    return atleta

@router.get(
    "/simplificado/",
    summary="Consultar todos os Atletas (resumo)",
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaSimplificadoOut],
)
async def query_simplificado(db_session: DatabaseDependency):
    result = await db_session.execute(
        select(AtletaModel)
        .options(
            joinedload(AtletaModel.centro_treinamento),
            joinedload(AtletaModel.categoria)
        )
    )
    atletas = result.scalars().unique().all()
    
    # Usamos paginate em vez de sqlalchemy_paginate para listas já carregadas
    return paginate([AtletaSimplificadoOut.from_model(atleta) for atleta in atletas])

@router.patch(
    "/{id}",
    summary="Editar um atleta pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Atleta com id: {id} não encontrado")

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
        
    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    "/{id}",
    summary="Deletar um atleta pelo ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def query(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Atleta com id: {id} não encontrado")

    await db_session.delete(atleta)
    await db_session.commit()

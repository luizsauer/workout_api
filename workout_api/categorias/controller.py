#workout_api\categorias\controller.py
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut, CategoriaUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from workout_api.atletas.models import AtletaModel
router = APIRouter()

@router.post(
    "/",
    summary="Cria uma nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, 
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    try:
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())
        
        db_session.add(categoria_model)
        await db_session.commit()

    
    except IntegrityError as e:
        await db_session.rollback()
        if "nome" in str(e).lower() or "categoria_nome_key" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f"Já existe uma categoria cadastrada com o nome: {categoria_in.nome}"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro de integridade ao inserir a categoria: {str(e)}"
        )

    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir a categoria: {str(e)}"
        )
    return categoria_out


@router.get(
    "/",
    summary="Consultar todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoriaOut],
)
async def query(db_session: DatabaseDependency):
    query = select(CategoriaModel)
    return await sqlalchemy_paginate(db_session, query)



@router.get(
    "/{id}",
    summary="Consultar uma categoria pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Categoria não encontrada no id: {id}")

    return categoria


@router.patch(
    "/{id}",
    summary="Editar uma categoria pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency, categoria_up: CategoriaUpdate = Body(...)) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Categoria com id: {id} não encontrado")

    categoria_update = categoria_up.model_dump(exclude_unset=True)
    for key, value in categoria_update.items():
        setattr(categoria, key, value)
        
    await db_session.commit()
    await db_session.refresh(categoria)

    return categoria


@router.delete(
    "/{id}",
    summary="Deletar uma categoria pelo ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def query(id: UUID4, db_session: DatabaseDependency) -> None:
    # categoria: CategoriaOut = (
    #     await db_session.execute(select(CategoriaModel).filter_by(id=id))
    # ).scalars().first()
    
    # Primeiro verifica se a categoria existe
    categoria = await db_session.get(CategoriaModel, id)
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Categoria com id: {id} não encontrada")

    # Verifica se há atletas associados a esta categoria
    result = await db_session.execute(select(AtletaModel).where(AtletaModel.categoria_id == categoria.pk_id))
    atletas_associados = result.scalars().all()

    if atletas_associados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar a categoria pois existem atletas associados a ela"
        )

    await db_session.delete(categoria)
    await db_session.commit()

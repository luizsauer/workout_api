#workout_api\routers.py
from fastapi import APIRouter
from workout_api.atletas.controller import router as atleta
from workout_api.categorias.controller import router as categorias
from workout_api.centro_treinamento.controller import router as centro_treinamento

api_router = APIRouter()
api_router.include_router(atleta, prefix="/atletas", tags=["atletas"])
api_router.include_router(categorias, prefix="/categorias", tags=["categorias"])
api_router.include_router(centro_treinamento, prefix="/centro_treinamento", tags=["centro_treinamento"])
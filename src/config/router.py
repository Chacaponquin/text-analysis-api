from fastapi import APIRouter
from src.modules.docs.controller import docs_router

app_router = APIRouter(prefix='/api')
app_router.include_router(prefix='/docs', router=docs_router)


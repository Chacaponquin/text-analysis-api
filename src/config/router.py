from fastapi import APIRouter
from src.modules.docs.controller import docs_router
from src.modules.category.controller import category_router
from src.modules.entity.controller import entity_router
from src.modules.report.controller import report_router

app_router = APIRouter(prefix='/api')
app_router.include_router(prefix='/docs', router=docs_router)
app_router.include_router(prefix='/category', router=category_router)
app_router.include_router(prefix='/entity', router=entity_router)
app_router.include_router(prefix='/report', router=report_router)

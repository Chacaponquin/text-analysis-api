from fastapi import APIRouter

from .services import CategoryServices
from .dto import FindCategory
from src.modules.docs.services import DocsServices


category_router = APIRouter()


@category_router.post('/find')
async def find_category(params: FindCategory):
    docs_services = DocsServices()
    services = CategoryServices(docs_services)
    return services.find_categories(params)

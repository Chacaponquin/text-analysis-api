from fastapi import APIRouter

from .services import CategoryServices
from .dto import FindCategory


category_router = APIRouter()


@category_router.post('/find')
async def find_category(params: FindCategory):
    services = CategoryServices()
    return services.find_categories(params)

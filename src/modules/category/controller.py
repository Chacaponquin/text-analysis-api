from fastapi import APIRouter
from pydantic import BaseModel
from .services import CategoryServices


category_router = APIRouter()


class FindCategory(BaseModel):
   category_name: str


@category_router.post('/find')
async def find_category(params: FindCategory):
    services = CategoryServices()
    return services.find_categories()

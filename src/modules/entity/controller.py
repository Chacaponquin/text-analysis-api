from fastapi import APIRouter
from pydantic import BaseModel
from .services import EntityServices


entity_router = APIRouter()


class FindEntity(BaseModel):
   entity_name: str


@entity_router.post('/find')
async def find_entity(params: FindEntity):
    services = EntityServices()
    return services.find_entities()
from fastapi import APIRouter
from .services import EntityServices
from .dto import FindEntity


entity_router = APIRouter()


@entity_router.post('/find')
async def find_entity(params: FindEntity):
    services = EntityServices()
    return services.find_entities(params)

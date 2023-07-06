from fastapi import APIRouter

from .services import EntityServices
from .dto import FindEntity
from src.modules.docs.services import DocsServices


entity_router = APIRouter()


@entity_router.post('/find')
async def find_entity(params: FindEntity):
    docs_services = DocsServices()
    services = EntityServices(docs_services)
    return services.find_entities(params)

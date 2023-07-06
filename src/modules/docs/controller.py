from fastapi import HTTPException, APIRouter, Body, Request
from .services import DocsServices
from .exceptions import FetchDocsError
from src.modules.shared.dto import FilterDTO


docs_router = APIRouter()


@docs_router.get('/all_docs')
def get_docs():
    try:
        docs_services = DocsServices()
        docs = docs_services.find_similar_documents()
        return docs
    except FetchDocsError:
        raise HTTPException(status_code=500)
    except Exception:
        raise HTTPException(status_code=500)


@docs_router.post('/find')
async def search_similar_documents(filter: FilterDTO):
    try:
        docs_services = DocsServices()
        docs = docs_services.find_similar_documents(filter)
        return docs
    except FetchDocsError:
        raise HTTPException(status_code=500)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500)
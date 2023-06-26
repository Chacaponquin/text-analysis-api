from fastapi import HTTPException, APIRouter, Body, Request
from .services import DocsServices
from .exceptions import FetchDocsError
from .dto import FindDocDTO


docs_router = APIRouter()


@docs_router.get('/all_docs')
def get_docs():
    try:
        docs_services = DocsServices()
        docs = docs_services.get_all_docs()
        return docs
    except FetchDocsError:
        raise HTTPException(status_code=500)
    except Exception:
        raise HTTPException(status_code=500)


@docs_router.post('/find')
async def search_similar_documents(params: FindDocDTO):
    try:
        docs_services = DocsServices()
        docs = docs_services.search_similar_documents(params)
        return docs
    except FetchDocsError:
        raise HTTPException(status_code=500)
    except Exception:
        raise HTTPException(status_code=500)
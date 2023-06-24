from fastapi import HTTPException, APIRouter
from .services import DocsServices
from .exceptions import FetchDocsError


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


@docs_router.get('/search/{doc_search}')
def search_similar_documents(search_doc: str):
    try:
        docs_services = DocsServices()
        docs = docs_services.search_similar_documents(search_doc)
        return docs
    except FetchDocsError:
        raise HTTPException(status_code=500)
    except Exception:
        raise HTTPException(status_code=500)
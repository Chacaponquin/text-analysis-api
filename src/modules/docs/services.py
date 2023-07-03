from .repository import DocsRepository
from src.modules.shared.dto import FilterDTO


class DocsServices:
    def __init__(self):
        self.repository = DocsRepository()

    def get_all_docs(self, docs_filter: FilterDTO | None = None):
        return self.repository.get_all_docs() if docs_filter is None else self.repository.find_similar_documents(docs_filter)


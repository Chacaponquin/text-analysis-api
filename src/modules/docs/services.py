from .repository import DocsReporsitory


class DocsServices:
    def __init__(self):
        self.repository = DocsReporsitory()

    def get_all_docs(self):
        return self.repository.get_all_docs()

    def search_similar_documents(self, search_doc: str):
        return self.repository.find_similar_documents(search_doc)


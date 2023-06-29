from src.modules.docs.services import DocsServices


class CategoryServices:
    def __init__(self):
        self.docs_services = DocsServices()

    def get_all_categories(self):
        all_docs = self.docs_services.get_all_docs()
        all_categories: list[str] = []

        for doc in all_docs:
            for cat in doc['categories']:
                if cat not in all_categories:
                    all_categories.append(cat)

        return all_categories

    def find_categories(self):
        categories = self.get_all_categories()
        return [{'category': c} for c in categories]
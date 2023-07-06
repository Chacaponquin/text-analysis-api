import difflib

from src.modules.shared.dto import FilterDTO
from .dto import FindCategory


class CategoryServices:
    def __init__(self, docs_services):
        self.docs_services = docs_services

    def found_category_by_name(self, categories, category_name):
        found = None

        for cat in categories:
            if cat['category'] == category_name:
                found = cat
                break

        return found

    def get_category_freq(self, filter_docs: FilterDTO, category_name) -> int:
        all_docs = self.docs_services.get_all_docs(filter_docs)
        count = 0

        for doc in all_docs:
            for cat in doc['doc']['categories']:
                if cat == category_name:
                    count += 1

        return count

    def get_all_categories(self, doc_filter: FilterDTO | None = None):
        all_docs = self.docs_services.get_all_docs(doc_filter)
        all_categories: list[dict] = []

        for doc in all_docs:
            for cat in doc['doc']['categories']:
                found_cat = self.found_category_by_name(all_categories, cat)
                if found_cat is None:
                    all_categories.append({'category': cat, 'count': 1})
                else:
                    found_cat['count'] = found_cat['count'] + 1

        return all_categories

    def _filter_category_by_name(self, categories, filter_category_name):
        for cat in categories:
            level_suggest = difflib.SequenceMatcher(None, filter_category_name, cat['category']).ratio()
            cat['suggest'] = level_suggest

        return categories

    def find_categories(self, params: FindCategory):
        categories = self.get_all_categories()
        categories = self._filter_category_by_name(categories, params.category_name)

        categories.sort(key=lambda x: x['suggest'], reverse=True)
        return categories[:10]

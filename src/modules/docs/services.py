import datetime
import difflib

from .repository import DocsRepository
from src.modules.shared.dto import FilterDTO
from src.modules.category.services import CategoryServices
from src.modules.category.domain import DocCategory
from src.modules.entity.domain import DocEntity
from src.modules.entity.services import EntityServices
from .domain import DocYearLimit


class DocsServices:
    def __init__(self):
        self.repository = DocsRepository()

        self.category_services = CategoryServices(self)
        self.entity_services = EntityServices(self)

        self.ENTITY_SUGGEST_LEVEL = 0.1
        self.CATEGORY_SUGGEST_LEVEL = 0.1
        self.TITLE_SUGGEST_LEVEL = 1

        self.SUGGEST_FIELD = 'suggest'

    def find_similar_documents(self, filter_docs: FilterDTO | None):
        return_docs = self.get_all_docs(filter_docs)
        return_docs_categories = self._get_filter_docs_categories(filter_docs, return_docs)
        return_docs_entities = self._get_filter_docs_entities(filter_docs, return_docs)
        return_docs_years_limit = self._get_filter_docs_years_limit(return_docs)

        return {'docs': return_docs, 'categories': return_docs_categories, 'entities': return_docs_entities, 'years': return_docs_years_limit}

    def get_all_docs(self, params: FilterDTO | None = None):
        all_docs = self.repository.get_all_docs()

        if params is not None:
            order_docs = self._filter_docs_by_title(all_docs, params.document_title)
            order_docs = self._filter_docs_by_entities(order_docs, params.entities)
            order_docs = self._filter_docs_by_categories(order_docs, params.categories)
            order_docs = self._filter_docs_by_years(order_docs, params.year_init, params.year_finish)

            order_docs.sort(key=lambda x: x[self.SUGGEST_FIELD], reverse=True)
            return order_docs
        else:
            return list(map(lambda x: {'doc': x, self.SUGGEST_FIELD: 0.0}, all_docs))

    def _get_filter_docs_years_limit(self, docs) -> DocYearLimit:
        year_limit = DocYearLimit()

        if len(docs) > 0:
            min_year: int = self.get_doc_year(docs[0]['doc']['date']).year
            max_year: int = self.get_doc_year(docs[0]['doc']['date']).year

            for i in range(1, len(docs)):
                current_doc = docs[i]
                current_doc_date = self.get_doc_year(current_doc['doc']['date'])

                if current_doc_date.year > max_year:
                    max_year = current_doc_date.year

                elif current_doc_date.year < min_year:
                    min_year = current_doc_date.year

            year_limit.year_init = min_year
            year_limit.year_finish = max_year

        return year_limit

    def _get_filter_docs_categories(self, filter_docs: FilterDTO, docs) -> list[DocCategory]:
        return_categories: list[DocCategory] = []

        for doc in docs:
            for cat in doc['doc']['categories']:
                if cat not in list(map(lambda x: x.category, return_categories)):
                    freq_category = self.category_services.get_category_freq(filter_docs, cat)
                    save_cat = DocCategory(cat, freq_category)
                    return_categories.append(save_cat)

        return return_categories

    def _get_filter_docs_entities(self, filter_docs: FilterDTO, docs) -> list[DocEntity]:
        return_entities: list[DocEntity] = []

        for doc in docs:
            for ent in doc['doc']['entities']:
                if ent not in list(map(lambda x: x.entity, return_entities)):
                    freq_entity = self.entity_services.get_entity_freq(filter_docs, ent)
                    save_entity = DocEntity(ent, freq_entity)
                    return_entities.append(save_entity)

        return return_entities

    def get_doc_year(self, doc_date) -> datetime:
        return datetime.datetime.strptime(doc_date, "%Y-%m-%dT%H:%M:%SZ")

    def _filter_docs_by_years(self, docs, year_init: int, year_finish: int):
        filter_docs = []

        for doc in docs:
            doc_date = self.get_doc_year(doc['doc']['date'])

            if doc_date.year >= year_init and doc_date.year <= year_finish:
                filter_docs.append(doc)

        return filter_docs

    def _filter_docs_by_categories(self, docs, filter_categories):
        return_docs = []

        for doc in docs:
            count = 0

            for f_cat in filter_categories:
                if f_cat in doc['doc']['categories']:
                    count += 1

            doc[self.SUGGEST_FIELD] += (count * self.CATEGORY_SUGGEST_LEVEL)

            if count == len(filter_categories):
                return_docs.append(doc)

        return return_docs

    def _filter_docs_by_entities(self, docs, filter_entities):
        return_docs = []

        for doc in docs:
            count = 0

            for f_ent in filter_entities:
                if f_ent in doc['doc']['entities']:
                    count += 1

            doc[self.SUGGEST_FIELD] += (count * self.ENTITY_SUGGEST_LEVEL)

            if len(filter_entities) == count:
                return_docs.append(doc)

        return return_docs

    def _filter_docs_by_title(self, docs, document_title):
        return_docs = []

        for doc in docs:
            current_doc_level_suggest = difflib.SequenceMatcher(None, document_title, doc['title']).ratio() * self.TITLE_SUGGEST_LEVEL
            return_docs.append({'doc': doc, self.SUGGEST_FIELD: current_doc_level_suggest})

        return return_docs

    def get_docs_over_time(self, docs_filter: FilterDTO):
        all_docs = self.get_all_docs(docs_filter)
        difference_years = docs_filter.year_finish - docs_filter.year_init

        if difference_years <= 1:
            return_data = []

            # months
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

            for m_index, month in enumerate(months):
                count_docs_in_month = 0
                month_original_index = m_index + 1

                for doc in all_docs:
                    doc_date = self.get_doc_year(doc['doc']['date'])

                    if doc_date.month == month_original_index:
                        count_docs_in_month += 1

                return_data.append({'unit': month, 'count': count_docs_in_month})

            return return_data

        else:
            return_data = []

            step = int(difference_years / 10) if int(difference_years / 10) > 0 else 1
            for year in range(docs_filter.year_init, docs_filter.year_finish + 1, step):
                count_docs_in_year = 0

                for doc in all_docs:
                    doc_date = self.get_doc_year(doc['doc']['date'])

                    if doc_date.year == year:
                        count_docs_in_year += 1

                return_data.append({'unit': str(year), 'count': count_docs_in_year})

            return return_data




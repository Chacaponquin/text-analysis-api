import requests
import difflib
import datetime

from .exceptions import FetchDocsError
from src.modules.shared.dto import FilterDTO


class DocsRepository:
    def __init__(self):
        self.get_url = 'http://localhost:8983/solr/docs/select?indent=true&q.op=OR&q=*%3A*&rows=1000&start=0'
        self.ENTITY_SUGGEST_LEVEL = 0.1
        self.CATEGORY_SUGGEST_LEVEL = 0.1
        self.TITLE_SUGGEST_LEVEL = 3

    def get_all_docs(self):
        session = requests.session()
        res = session.get(self.get_url, headers={'Content-Type': 'application/json'})

        if not res.ok:
            raise FetchDocsError()

        return self._map_docs(res.json()['response']['docs'])

    def find_similar_documents(self, params: FilterDTO | None = None):
        all_docs = self.get_all_docs()

        if params is not None:
            order_docs = self._filter_docs_by_title(all_docs, params.document_title)
            order_docs = self._filter_docs_by_entities(order_docs, params.entities)
            order_docs = self._filter_docs_by_categories(order_docs, params.categories)
            order_docs = self._filter_docs_by_years(order_docs, params.year_init, params.year_finish)

            order_docs.sort(key=lambda x: x['suggest'], reverse=True)
            return order_docs
        else:
            return list(map(lambda x: {'doc': x, 'suggest': 0.0}, all_docs))

    def _filter_docs_by_years(self, docs, year_init: int, year_finish: int):
        filter_docs = []

        for doc in docs:
            doc_date = datetime.datetime.strptime(doc['doc']['date'], "%Y-%m-%dT%H:%M:%SZ")

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

            if len(filter_entities) == count:
                return_docs.append(doc)

        return return_docs

    def _filter_docs_by_title(self, docs, document_title):
        return_docs = []

        for doc in docs:
            current_doc_level_suggest = difflib.SequenceMatcher(None, document_title, doc['title']).ratio() * self.TITLE_SUGGEST_LEVEL
            return_docs.append({'doc': doc, 'suggest': current_doc_level_suggest})

        return return_docs

    def _map_docs(self, docs):
        return_docs = []

        for d in docs:
            try:
                newDoc = {}
                newDoc['id'] = d['id']
                newDoc['title'] = d['title'][0]
                newDoc['content'] = d['content'][0]
                newDoc['date'] = d['date'][0]
                newDoc['entities'] = d['entity']
                newDoc['categories'] = d['category']
                newDoc['author'] = d['author'][0]

                return_docs.append(newDoc)
            except Exception:
                pass

        return return_docs

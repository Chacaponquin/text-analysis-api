import requests
import difflib
from .exceptions import FetchDocsError


class DocsReporsitory:
    def get_all_docs(self):
        session = requests.session()
        res = session.get("http://localhost:8983/solr/articulo/select?indent=true&q.op=OR&q=*%3A*&rows=100&start=0", headers={'Content-Type': 'application-type'})

        if not res.ok:
            raise FetchDocsError()

        return self._map_docs(res.json()['response']['docs'])

    def find_similar_documents(self, search_title: str):
        search_docs = []
        for doc in self.get_all_docs():
            if difflib.SequenceMatcher(None, search_title, doc['title']).ratio() > 0.7:
                search_docs.append(doc)
        return search_docs


    def _map_docs(self, docs):
        return_docs = []

        for d in docs:
            try:
                newDoc = {}
                newDoc['id'] = d['id']
                newDoc['title'] = d['title'][0]
                newDoc['text'] = d['text'][0]
                newDoc['date'] = d['date'][0]

                return_docs.append(newDoc)
            except Exception:
                pass

        return return_docs

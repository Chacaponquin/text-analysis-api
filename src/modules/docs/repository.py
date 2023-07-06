import requests

from .exceptions import FetchDocsError


class DocsRepository:
    def __init__(self):
        self.get_url = 'http://localhost:8983/solr/docs/select?indent=true&q.op=OR&q=*%3A*&rows=1000&start=0'

    def get_all_docs(self):
        session = requests.session()
        res = session.get(self.get_url, headers={'Content-Type': 'application/json'})

        if not res.ok:
            raise FetchDocsError()

        return self._map_docs(res.json()['response']['docs'])

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

import requests
import random
import datetime

from .exceptions import FetchDocsError
from src.config.env import ENVS


class DocsRepository:
    def __init__(self):
        self.get_url = f'http://localhost:8983/solr/{ENVS.DATABASE}/select?indent=true&q.op=OR&q=*%3A*&rows=100000&start=0'

    def get_all_docs(self):
        session = requests.session()
        res = session.get(self.get_url, headers={'Content-Type': 'application/json'})

        if not res.ok:
            raise FetchDocsError()

        return self._map_docs(res.json()['response']['docs'])

    def _map_docs(self, docs):
        return_docs = []

        for d in docs:
            newDoc = {}
            newDoc['id'] = d['id']
            newDoc['title'] = d['title'][0]
            newDoc['content'] = d['content'][0]
            newDoc['date'] = d['date'][0]
            newDoc['entities'] = d['entities']
            newDoc['categories'] = d['categories']
            newDoc['author'] = d['author'][0]

            return_docs.append(newDoc)

        return return_docs

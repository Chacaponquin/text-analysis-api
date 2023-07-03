from src.modules.docs.services import DocsServices
import difflib

from .dto import FindEntity
from src.modules.shared.dto import FilterDTO


class EntityServices:
    def __init__(self):
        self.docs_services = DocsServices()

    def exists_entity_by_name(self, entities, entity_name):
        found = False

        for ent in entities:
            if ent['entity'] == entity_name:
                found = True
                break

        return found

    def found_entity_by_name(self, entities, entity_name):
        for ent in entities:
            if ent['entity'] == entity_name:
                return ent

    def get_all_entities(self, docs_filter: FilterDTO | None = None) -> list[dict]:
        all_docs = self.docs_services.get_all_docs(docs_filter)
        all_entities: list[dict] = []

        for doc in all_docs:
            for ent in doc['entities']:
                if not self.exists_entity_by_name(all_entities, ent):
                    all_entities.append({'entity': ent, 'count': 0})
                else:
                    found_entity = self.found_entity_by_name(all_entities, ent)
                    found_entity['count'] = found_entity['count'] + 1

        return all_entities

    def _filter_entities_by_name(self, entities, filter_entity_name):
        for ent in entities:
            level_suggest = difflib.SequenceMatcher(None, filter_entity_name, ent['entity']).ratio()
            ent['suggest'] = level_suggest

        return entities

    def find_entities(self, params: FindEntity):
        entities = self.get_all_entities()
        entities = self._filter_entities_by_name(entities, params.entity_name)

        entities.sort(reverse=True, key=lambda x: x['suggest'])
        return entities[:10]

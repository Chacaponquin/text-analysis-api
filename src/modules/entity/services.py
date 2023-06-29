from src.modules.docs.services import DocsServices


class EntityServices:
    def __init__(self):
        self.docs_services = DocsServices()

    def get_all_entities(self):
        all_docs = self.docs_services.get_all_docs()
        all_entities: list[str] = []

        for doc in all_docs:
            for ent in doc['entities']:
                if ent not in all_entities:
                    all_entities.append(ent)

        return all_entities

    def find_entities(self):
        entities = self.get_all_entities()
        return [{'entity': e} for e in entities]
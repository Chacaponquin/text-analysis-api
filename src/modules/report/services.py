from src.modules.entity.services import EntityServices
from src.modules.shared.dto import FilterDTO


class ReportServices:
    def __init__(self):
        self.entity_services = EntityServices()

    def get_entity_frequency_data(self, docs_filter: FilterDTO | None = None):
        all_entities = self.entity_services.get_all_entities(docs_filter)
        return all_entities

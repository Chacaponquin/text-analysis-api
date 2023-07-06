from src.modules.entity.services import EntityServices
from src.modules.shared.dto import FilterDTO
from src.modules.category.services import CategoryServices
from src.modules.docs.services import DocsServices


class ReportServices:
    def __init__(self):
        self.docs_services = DocsServices()
        self.entity_services = EntityServices(self.docs_services)
        self.category_services = CategoryServices(self.docs_services)

    def get_entity_frequency_data(self, docs_filter: FilterDTO):
        all_entities = self.entity_services.get_all_entities(docs_filter)
        all_entities.sort(key=lambda x: x['count'], reverse=True)
        return all_entities

    def get_category_frequence_data(self, docs_filter: FilterDTO):
        all_categories = self.category_services.get_all_categories(docs_filter)
        return all_categories

    def get_entity_over_time_data(self, docs_filter: FilterDTO):
        data = self.entity_services.get_entities_over_time(docs_filter)
        return data

    def get_docs_over_time(self, docs_filter: FilterDTO):
        data = self.docs_services.get_docs_over_time(docs_filter)
        return data


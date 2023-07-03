from src.modules.entity.services import EntityServices
from src.modules.shared.dto import FilterDTO
from src.modules.category.services import CategoryServices


class ReportServices:
    def __init__(self):
        self.entity_services = EntityServices()
        self.category_services = CategoryServices()

    def get_entity_frequency_data(self, docs_filter: FilterDTO):
        all_entities = self.entity_services.get_all_entities(docs_filter)
        return all_entities

    def get_category_frequence_data(self, docs_filter: FilterDTO):
        all_categories = self.category_services.get_all_categories(docs_filter)
        return all_categories

    def get_entity_over_time_data(self, docs_filter: FilterDTO):
        data = self.entity_services.get_entities_over_time(docs_filter)
        return data


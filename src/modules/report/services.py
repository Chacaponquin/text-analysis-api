from src.modules.entity.services import EntityServices
from src.modules.shared.dto import FilterDTO
from src.modules.category.services import CategoryServices
from src.modules.docs.services import DocsServices
from .domain import ReportEntityRelations, EntityRelation


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

    def get_entities_corelation(self, docs_filter: FilterDTO, root_entity: str) -> ReportEntityRelations:
        return_data = ReportEntityRelations(root_entity)
        all_docs = self.docs_services.get_all_docs(docs_filter)

        for doc in all_docs:
            if root_entity in doc['doc']['entities']:
                for ent in doc['doc']['entities']:
                    if ent != root_entity:
                        found_relation = return_data.check_entity_in_relations(ent)
                        if found_relation is None:
                            new_relation = EntityRelation(ent)
                            return_data.relations.append(new_relation)
                        else:
                            found_relation.count += 1

        return_data.relations.sort(reverse=True, key=lambda x: x.count)
        return return_data


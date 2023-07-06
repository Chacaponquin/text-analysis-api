import datetime
import difflib

from .dto import FindEntity
from src.modules.shared.dto import FilterDTO


class EntityServices:
    def __init__(self, docs_services):
        self.docs_services = docs_services

    def exists_entity_by_name(self, entities, entity_name):
        found = False

        for ent in entities:
            if ent['entity'] == entity_name:
                found = True
                break

        return found

    def found_entity_by_name(self, entities, entity_name):
        found = None

        for ent in entities:
            if ent['entity'] == entity_name:
                found = ent
                break

        return found

    def get_entity_freq(self, filter_docs: FilterDTO, entity_name: str) -> int:
        count = 0
        all_docs = self.docs_services.get_all_docs(filter_docs)

        for doc in all_docs:
            for ent in doc['doc']['entities']:
                if ent == entity_name:
                    count += 1

        return count

    def get_entities_over_time(self, docs_filter: FilterDTO | None = None):
        all_docs = self.docs_services.get_all_docs(docs_filter)
        all_entities: list[dict] = []

        difference_years = docs_filter.year_finish - docs_filter.year_init

        for doc in all_docs:
            for ent in doc['doc']['entities']:
                if not self.exists_entity_by_name(all_entities, ent):
                    all_entities.append({'entity': ent, 'time_data': []})

        if difference_years <= 1:
            # months
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

            for ent in all_entities:
                save_entity_months_data = []
                for m_index, month in enumerate(months):
                    count_entity_repeat = 0
                    month_original_index = m_index + 1

                    for doc in all_docs:
                        doc_date = datetime.datetime.strptime(doc['doc']['date'], "%Y-%m-%dT%H:%M:%SZ")
                        doc_include_entity = ent['entity'] in doc['doc']['entities']

                        if doc_date.month == month_original_index and doc_include_entity:
                            count_entity_repeat += 1

                    save_entity_months_data.append({'count': count_entity_repeat, 'unit': months[m_index]})

                ent['time_data'] = save_entity_months_data

        else:
            for ent in all_entities:
                save_entity_months_data = []

                step = int(difference_years / 10) if int(difference_years / 10) > 0 else 1
                for year in range(docs_filter.year_init, docs_filter.year_finish + 1, step):
                    count_entity_repeat = 0

                    for doc in all_docs:
                        doc_date = datetime.datetime.strptime(doc['doc']['date'], "%Y-%m-%dT%H:%M:%SZ")
                        doc_include_entity = ent['entity'] in doc['doc']['entities']

                        if doc_date.year == year and doc_include_entity:
                            count_entity_repeat += 1

                    save_entity_months_data.append({'count': count_entity_repeat, 'unit': str(year)})

                ent['time_data'] = save_entity_months_data

        return all_entities

    def get_all_entities(self, docs_filter: FilterDTO | None = None) -> list[dict]:
        all_docs = self.docs_services.get_all_docs(docs_filter)
        all_entities: list[dict] = []

        for doc in all_docs:
            for ent in doc['doc']['entities']:
                if not self.exists_entity_by_name(all_entities, ent):
                    all_entities.append({'entity': ent, 'count': 1})
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

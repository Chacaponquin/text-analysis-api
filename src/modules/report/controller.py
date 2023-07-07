from fastapi import APIRouter

from .services import ReportServices
from src.modules.shared.dto import FilterDTO
from .dto import ReportEntityRelationsDTO


report_router = APIRouter()


@report_router.post('/entity_frequency')
def get_entity_frequency(docs_filter: FilterDTO):
    report_services = ReportServices()
    return report_services.get_entity_frequency_data(docs_filter)


@report_router.post('/category_frequency')
def get_category_frequency(docs_filter: FilterDTO):
    report_services = ReportServices()
    return report_services.get_category_frequence_data(docs_filter)


@report_router.post('/entity_over_time')
def get_entity_over_time(docs_filter: FilterDTO):
    report_services = ReportServices()
    return report_services.get_entity_over_time_data(docs_filter)


@report_router.post('/docs_over_time')
def get_docs_over_time(docs_filter: FilterDTO):
    report_services = ReportServices()
    return report_services.get_docs_over_time(docs_filter)

@report_router.post('/entity_relations')
def get_entity_relations(report_dto: ReportEntityRelationsDTO):
    report_services = ReportServices()
    return report_services.get_entities_corelation(report_dto.docs_filter, report_dto.root_entity)
